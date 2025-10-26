#!/usr/bin/env python
"""
Automatic colorization from reference image using feature point matching.

This module detects unique feature points in a reference image and transfers
their colors to corresponding points in a grayscale image for automatic colorization.

Usage:
    conda activate rvrt
    python auto_colorize_from_reference.py --gray_image input.jpg --ref_image reference.jpg
"""

import cv2
import numpy as np
import argparse
from sklearn.cluster import KMeans
from skimage import color


class AutoColorizeFromReference:
    """Automatic colorization using reference image feature matching"""
    
    def __init__(self, method='orb', num_points=50, match_threshold=0.7):
        """
        Initialize the auto-colorizer
        
        Args:
            method: Feature detection method ('orb', 'sift', 'akaze')
            num_points: Maximum number of color points to extract
            match_threshold: Matching threshold (0-1, lower is stricter)
        """
        self.method = method.lower()
        self.num_points = num_points
        self.match_threshold = match_threshold
        self.detector = None
        self.matcher = None
        self._init_detector()
    
    def _init_detector(self):
        """Initialize feature detector and matcher"""
        if self.method == 'sift':
            try:
                self.detector = cv2.SIFT_create()
                self.matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
            except:
                print("SIFT not available, falling back to ORB")
                self.method = 'orb'
        
        if self.method == 'orb':
            self.detector = cv2.ORB_create(nfeatures=500)
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        
        elif self.method == 'akaze':
            self.detector = cv2.AKAZE_create()
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    
    def detect_features(self, image):
        """
        Detect feature points in an image
        
        Args:
            image: Grayscale image
            
        Returns:
            keypoints, descriptors
        """
        keypoints, descriptors = self.detector.detectAndCompute(image, None)
        return keypoints, descriptors
    
    def match_features(self, desc1, desc2):
        """
        Match features between two images
        
        Args:
            desc1: Descriptors from first image
            desc2: Descriptors from second image
            
        Returns:
            List of good matches
        """
        if desc1 is None or desc2 is None:
            return []
        
        # Use KNN matching
        matches = self.matcher.knnMatch(desc1, desc2, k=2)
        
        # Apply ratio test (Lowe's ratio test)
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < self.match_threshold * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    def cluster_points(self, points, n_clusters):
        """
        Cluster points to get representative samples
        
        Args:
            points: Array of points (N, 2)
            n_clusters: Number of clusters
            
        Returns:
            Cluster centers
        """
        if len(points) <= n_clusters:
            return points
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(points)
        return kmeans.cluster_centers_.astype(int)
    
    def extract_color_points(self, gray_image, ref_image, visualize=False):
        """
        Extract color points from reference image and match to grayscale image
        
        Args:
            gray_image: Grayscale image (H, W) or (H, W, 3)
            ref_image: Reference color image (H, W, 3)
            visualize: Whether to return visualization
            
        Returns:
            color_points: List of (x, y, r, g, b) tuples
            vis_image: Visualization image (if visualize=True)
        """
        # Ensure grayscale
        if len(gray_image.shape) == 3:
            gray_img = cv2.cvtColor(gray_image, cv2.COLOR_RGB2GRAY)
        else:
            gray_img = gray_image
        
        # Convert reference to grayscale for feature detection
        ref_gray = cv2.cvtColor(ref_image, cv2.COLOR_RGB2GRAY)
        
        # Detect features
        print(f"Detecting features using {self.method.upper()}...")
        kp_gray, desc_gray = self.detect_features(gray_img)
        kp_ref, desc_ref = self.detect_features(ref_gray)
        
        print(f"Found {len(kp_gray)} keypoints in grayscale image")
        print(f"Found {len(kp_ref)} keypoints in reference image")
        
        # Match features
        print("Matching features...")
        matches = self.match_features(desc_gray, desc_ref)
        print(f"Found {len(matches)} good matches")
        
        if len(matches) == 0:
            print("Warning: No matches found!")
            return [], None
        
        # Extract matched point coordinates
        matched_points_gray = []
        matched_colors = []
        
        for match in matches:
            # Get coordinates in grayscale image
            pt_gray = kp_gray[match.queryIdx].pt
            x_gray, y_gray = int(pt_gray[0]), int(pt_gray[1])
            
            # Get coordinates in reference image
            pt_ref = kp_ref[match.trainIdx].pt
            x_ref, y_ref = int(pt_ref[0]), int(pt_ref[1])
            
            # Check bounds
            if (0 <= x_gray < gray_img.shape[1] and 0 <= y_gray < gray_img.shape[0] and
                0 <= x_ref < ref_image.shape[1] and 0 <= y_ref < ref_image.shape[0]):
                
                # Get color from reference image
                color_rgb = ref_image[y_ref, x_ref]
                
                matched_points_gray.append([x_gray, y_gray])
                matched_colors.append(color_rgb)
        
        if len(matched_points_gray) == 0:
            print("Warning: No valid matched points!")
            return [], None
        
        matched_points_gray = np.array(matched_points_gray)
        matched_colors = np.array(matched_colors)
        
        # Cluster points to get representative samples
        print(f"Clustering to {self.num_points} representative points...")
        if len(matched_points_gray) > self.num_points:
            cluster_centers = self.cluster_points(matched_points_gray, self.num_points)
            
            # For each cluster center, find nearest matched point and use its color
            color_points = []
            for center in cluster_centers:
                # Find nearest matched point
                distances = np.sum((matched_points_gray - center) ** 2, axis=1)
                nearest_idx = np.argmin(distances)
                
                x, y = matched_points_gray[nearest_idx]
                r, g, b = matched_colors[nearest_idx]
                color_points.append((int(x), int(y), int(r), int(g), int(b)))
        else:
            color_points = [(int(x), int(y), int(r), int(g), int(b)) 
                           for (x, y), (r, g, b) in zip(matched_points_gray, matched_colors)]
        
        print(f"Extracted {len(color_points)} color points")
        
        # Create visualization if requested
        vis_image = None
        if visualize:
            vis_image = self._create_visualization(gray_image, ref_image, color_points, matches, kp_gray, kp_ref)
        
        return color_points, vis_image
    
    def _create_visualization(self, gray_image, ref_image, color_points, matches, kp_gray, kp_ref):
        """Create visualization of matched points"""
        # Convert grayscale to RGB for visualization
        if len(gray_image.shape) == 2:
            gray_rgb = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        else:
            gray_rgb = gray_image.copy()
        
        # Draw color points on grayscale image
        vis_gray = gray_rgb.copy()
        for x, y, r, g, b in color_points:
            cv2.circle(vis_gray, (x, y), 5, (int(r), int(g), int(b)), -1)
            cv2.circle(vis_gray, (x, y), 6, (255, 255, 255), 1)
        
        # Draw matches
        vis_matches = cv2.drawMatches(
            gray_rgb, kp_gray, ref_image, kp_ref, 
            matches[:50],  # Show first 50 matches
            None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        
        # Combine visualizations
        h1, w1 = vis_gray.shape[:2]
        h2, w2 = vis_matches.shape[:2]
        
        # Resize to same width
        if w1 != w2:
            scale = w2 / w1
            vis_gray = cv2.resize(vis_gray, (w2, int(h1 * scale)))
        
        vis_combined = np.vstack([vis_gray, vis_matches])
        
        return vis_combined


def main():
    parser = argparse.ArgumentParser(description='Auto-colorize from reference image')
    parser.add_argument('--gray_image', type=str, required=True, help='Grayscale image to colorize')
    parser.add_argument('--ref_image', type=str, required=True, help='Reference color image')
    parser.add_argument('--method', type=str, default='orb', choices=['orb', 'sift', 'akaze'],
                        help='Feature detection method')
    parser.add_argument('--num_points', type=int, default=50, help='Number of color points to extract')
    parser.add_argument('--match_threshold', type=float, default=0.7, help='Matching threshold (0-1)')
    parser.add_argument('--output', type=str, default='color_points.txt', help='Output file for color points')
    parser.add_argument('--visualize', action='store_true', help='Save visualization')
    
    args = parser.parse_args()
    
    # Load images
    print(f"Loading grayscale image: {args.gray_image}")
    gray_img = cv2.imread(args.gray_image)
    if gray_img is None:
        print(f"Error: Could not load {args.gray_image}")
        return
    
    print(f"Loading reference image: {args.ref_image}")
    ref_img = cv2.imread(args.ref_image)
    if ref_img is None:
        print(f"Error: Could not load {args.ref_image}")
        return
    
    # Convert BGR to RGB
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB)
    ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)
    
    # Resize images to same size if needed
    if gray_img.shape[:2] != ref_img.shape[:2]:
        print(f"Resizing reference image to match grayscale image size...")
        ref_img = cv2.resize(ref_img, (gray_img.shape[1], gray_img.shape[0]))
    
    # Create auto-colorizer
    auto_colorizer = AutoColorizeFromReference(
        method=args.method,
        num_points=args.num_points,
        match_threshold=args.match_threshold
    )
    
    # Extract color points
    color_points, vis_image = auto_colorizer.extract_color_points(
        gray_img, ref_img, visualize=args.visualize
    )
    
    if len(color_points) == 0:
        print("No color points extracted!")
        return
    
    # Save color points
    print(f"\nSaving color points to {args.output}")
    with open(args.output, 'w') as f:
        f.write("# x, y, r, g, b\n")
        for x, y, r, g, b in color_points:
            f.write(f"{x}, {y}, {r}, {g}, {b}\n")
    
    print(f"Saved {len(color_points)} color points")
    
    # Save visualization
    if args.visualize and vis_image is not None:
        vis_path = args.output.replace('.txt', '_visualization.png')
        cv2.imwrite(vis_path, cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR))
        print(f"Saved visualization to {vis_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("Summary:")
    print("="*60)
    print(f"Grayscale image: {args.gray_image}")
    print(f"Reference image: {args.ref_image}")
    print(f"Method: {args.method.upper()}")
    print(f"Color points extracted: {len(color_points)}")
    print(f"Output file: {args.output}")
    print("="*60)
    
    # Print first few points as example
    print("\nFirst 5 color points:")
    for i, (x, y, r, g, b) in enumerate(color_points[:5]):
        print(f"  {i+1}. Position ({x}, {y}) -> Color RGB({r}, {g}, {b})")


if __name__ == '__main__':
    main()
