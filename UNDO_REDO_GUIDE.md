# Undo/Redo Feature Guide

## Overview
The iDeepColor application now includes full undo/redo functionality, allowing you to step backward and forward through your colorization history. This makes it easy to experiment with different color placements without fear of losing your work.

## Features

### Undo
- **Reverts the last action** you performed
- Supports up to **50 undo steps**
- Works for:
  - Adding new color points
  - Removing color points
  - (Point movements are tracked as part of the point state)

### Redo
- **Restores actions** that were undone
- Allows you to step forward through your history
- Redo history is cleared when you perform a new action

## How to Use

### Using Buttons
Located in the Drawing Pad menu bar:
- **Undo Button**: Click to undo the last action
- **Redo Button**: Click to redo the last undone action
- Buttons are automatically enabled/disabled based on availability

### Using Keyboard Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| **Ctrl+Z** | Undo | Undo the last action |
| **Ctrl+Y** | Redo | Redo the last undone action |
| **Ctrl+Shift+Z** | Redo | Alternative redo shortcut |

### Button States
- **Enabled** (clickable): Action is available
- **Disabled** (grayed out): No action available
  - Undo disabled: No actions to undo
  - Redo disabled: No actions to redo

## Workflow Examples

### Example 1: Experimenting with Colors
```
1. Add a blue point on the sky
2. Add a green point on grass
3. Don't like the grass color?
4. Press Ctrl+Z to undo the grass point
5. Select a different green
6. Add the new grass point
```

### Example 2: Trying Different Approaches
```
1. Add 5 points with one color scheme
2. Review the result
3. Press Ctrl+Z five times to remove all points
4. Try a completely different color scheme
5. Changed your mind?
6. Press Ctrl+Y five times to restore original points
```

### Example 3: Incremental Refinement
```
1. Add base colors across the image
2. Add detail points
3. Undo the last few detail points (Ctrl+Z)
4. Try different detail colors
5. Keep undoing/redoing until satisfied
```

## What Actions Are Tracked?

### Tracked Actions (Can Undo/Redo)
✅ **Adding new color points**
- When you left-click to add a new point
- Saves the state before adding

✅ **Removing color points**
- When you right-click to remove a point
- Saves the state before removing

### Not Tracked (Cannot Undo/Redo)
❌ **Color selection**
- Selecting colors from palettes
- Changing the current color

❌ **View changes**
- Toggling grayscale view
- Zooming or panning

❌ **File operations**
- Loading images
- Saving results

❌ **Point movements**
- Moving existing points (considered part of the point state)

## Technical Details

### History Limit
- **Maximum undo steps**: 50
- Oldest actions are automatically removed when limit is reached
- This prevents excessive memory usage

### Memory Usage
- Each undo state stores a copy of all points
- Typical memory per state: ~1-10 KB
- Total history memory: ~50-500 KB (negligible)

### State Storage
Each undo state includes:
- All color points (position, color, size)
- Point count
- Point metadata

### Performance
- **Undo/Redo speed**: Instant (<1ms)
- **No impact** on colorization speed
- **Minimal memory** overhead

## Tips & Best Practices

### General Tips
1. **Experiment freely**: Undo makes it safe to try different approaches
2. **Use keyboard shortcuts**: Much faster than clicking buttons
3. **Check button states**: Know when undo/redo is available
4. **Don't rely on redo**: New actions clear redo history

### Workflow Tips
1. **Save checkpoints**: Use Save button before major changes
2. **Undo in batches**: Hold Ctrl+Z to quickly undo multiple steps
3. **Compare versions**: Undo to see before/after
4. **Iterative refinement**: Add, review, undo, adjust, repeat

### Advanced Techniques

#### A/B Testing Colors
```
1. Add points with Color Scheme A
2. Review result
3. Undo all points (Ctrl+Z repeatedly)
4. Add points with Color Scheme B
5. Review result
6. Redo to restore Scheme A if preferred
```

#### Selective Undo
```
1. Add 10 points across image
2. Realize last 3 points are wrong
3. Press Ctrl+Z three times
4. Add correct points
5. Continue with confidence
```

#### Quick Experiments
```
1. Have a good base colorization
2. Try adding experimental detail points
3. If they don't work, quickly undo them
4. Try different approach
5. Keep what works
```

## Troubleshooting

### Q: Undo button is grayed out
**A:** No actions to undo. This happens when:
- You just started the application
- You just reset (R key)
- You've undone all available actions

### Q: Redo button is grayed out
**A:** No actions to redo. This happens when:
- You haven't undone anything yet
- You performed a new action after undoing (clears redo history)

### Q: Can't undo past a certain point
**A:** You've reached the 50-step history limit. Oldest actions are automatically removed.

### Q: Undo doesn't restore the exact color
**A:** Undo restores point positions and colors. The AI colorization may vary slightly due to:
- Different random seeds
- Model state
- This is normal and usually imperceptible

### Q: Lost my redo history
**A:** Redo history is cleared when you perform any new action. This is standard undo/redo behavior.

## Keyboard Shortcuts Summary

| Key | Action |
|-----|--------|
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+Shift+Z | Redo (alternative) |
| R | Reset all |
| S | Save |
| L | Load image |
| G | Toggle grayscale |
| Q | Save and quit |
| F11 | Toggle fullscreen |

## Comparison: Before vs After

### Before Undo/Redo
- ❌ Mistakes were permanent
- ❌ Had to manually remove wrong points
- ❌ Couldn't compare different approaches
- ❌ Risky to experiment
- ❌ Had to restart for major changes

### With Undo/Redo
- ✅ Mistakes are easily reversible
- ✅ Quick experimentation
- ✅ Compare different color schemes
- ✅ Safe to try new ideas
- ✅ Iterative refinement workflow

## Future Enhancements

Potential improvements:
- [ ] Visual undo/redo history timeline
- [ ] Named checkpoints/bookmarks
- [ ] Undo/redo for color changes
- [ ] Branching history (multiple undo paths)
- [ ] Undo history export/import
- [ ] Undo preview (show what will be undone)

## Summary

The undo/redo feature provides:
- ✅ **Safety**: Experiment without fear
- ✅ **Flexibility**: Try different approaches
- ✅ **Efficiency**: Quick corrections
- ✅ **Confidence**: Easy to fix mistakes
- ✅ **Workflow**: Iterative refinement

**Start using undo/redo to colorize with confidence!** 🎨
