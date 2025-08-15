# Gap Buffer Text Editor

A simple text editor that demonstrates how the **Gap Buffer** data structure works in real text editors!

## What is a Gap Buffer?

A gap buffer is a clever data structure used in text editors that maintains a "gap" of empty space at the current cursor position. This makes inserting and deleting text very efficient!

### How it Works:
- **Start Buffer**: Text before the cursor
- **Gap**: Empty space at the cursor position  
- **End Buffer**: Text after the cursor
- **Gap Index**: Where the gap starts
- **Gap Length**: How much empty space is available

## Features

✅ **Real Gap Buffer Implementation** - See the data structure in action!  
✅ **Basic Text Editing** - Type, delete, move cursor  
✅ **File Operations** - Open, save, new files  
✅ **Buffer Statistics** - View the gap buffer state  
✅ **Simple GUI** - Easy to use interface  

## How to Run

### Prerequisites
- Python 3.x (comes with tkinter)

### Run the Editor
```bash
python simple_text_editor.py
```

## Understanding the Gap Buffer

### When You Type:
1. Character goes into the gap
2. Gap gets smaller
3. Cursor moves right

### When You Move Cursor:
1. Gap "moves" with the cursor
2. Text shifts between start and end buffers
3. Gap stays at cursor position

### When You Delete:
1. Text moves into the gap
2. Gap gets bigger
3. No need to shift entire buffer!

## Try This!

1. **Type some text** - Watch the gap shrink
2. **Move cursor around** - See the gap move with you
3. **Delete characters** - Watch the gap grow
4. **View → Buffer Stats** - See the internal state
5. **Open a large file** - Notice how it handles big documents

## Why This Matters

This is how many real text editors work! The gap buffer makes editing efficient by:
- **Fast inserts** at cursor (O(1) amortized)
- **Efficient cursor movement** 
- **No massive text shifting** for small edits
- **Memory efficient** for typical editing patterns

## Next Steps

Want to learn more? Try:
- Implementing **selection** (highlighting text)
- Adding **undo/redo** functionality
- Implementing **search and replace**
- Adding **syntax highlighting**

## Code Structure

- `GapBuffer` class - The core data structure
- `SimpleTextEditor` class - GUI and user interaction
- `main()` function - Entry point

The gap buffer handles all text operations, while the GUI just displays the results!

---

**This is a learning tool** - it shows the fundamental concepts that power real text editors like Emacs, Vim, and many others!
