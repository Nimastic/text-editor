import tkinter as tk
from tkinter import messagebox
import sys

class GapBuffer:
    """A simple gap buffer implementation for text editing"""
    
    def __init__(self, initial_text="", buffer_size=1000):
        self.buffer_size = buffer_size
        self.start_buffer = list(initial_text)
        self.gap_index = len(initial_text)
        self.gap_length = buffer_size - len(initial_text)
        self.end_buffer = []
        
    def get_text(self):
        """Get the complete text from the buffer"""
        return ''.join(self.start_buffer + self.end_buffer)
    
    def insert(self, char):
        """Insert a character at the current gap position"""
        if self.gap_length == 0:
            self._expand_gap()
        
        self.start_buffer.append(char)
        self.gap_index += 1
        self.gap_length -= 1
    
    def delete(self):
        """Delete character before the gap (backspace)"""
        if self.gap_index > 0:
            self.gap_index -= 1
            self.gap_length += 1
            return self.start_buffer.pop()
        return None
    
    def delete_forward(self):
        """Delete character after the gap (delete key)"""
        if self.end_buffer:
            self.gap_length += 1
            return self.end_buffer.pop(0)
        return None
    
    def move_cursor_left(self):
        """Move cursor left (move gap left)"""
        if self.gap_index > 0:
            self.gap_index -= 1
            self.gap_length += 1
            # Move character from start to end
            char = self.start_buffer.pop()
            self.end_buffer.insert(0, char)
    
    def move_cursor_right(self):
        """Move cursor right (move gap right)"""
        if self.end_buffer:
            self.gap_length -= 1
            self.gap_index += 1
            # Move character from end to start
            char = self.end_buffer.pop(0)
            self.start_buffer.append(char)
    
    def move_cursor_to(self, position):
        """Move cursor to specific position"""
        current_pos = self.gap_index
        if position < current_pos:
            # Move left
            while self.gap_index > position:
                self.move_cursor_left()
        elif position > current_pos:
            # Move right
            while self.gap_index < position:
                self.move_cursor_right()
    
    def _expand_gap(self):
        """Expand the gap when it's full"""
        new_buffer_size = self.buffer_size * 2
        new_start = self.start_buffer + [''] * (new_buffer_size - self.buffer_size)
        self.start_buffer = new_start
        self.gap_length += new_buffer_size - self.buffer_size
        self.buffer_size = new_buffer_size
    
    def get_cursor_position(self):
        """Get current cursor position"""
        return self.gap_index
    
    def get_stats(self):
        """Get buffer statistics for debugging"""
        return {
            'start_length': len(self.start_buffer),
            'gap_length': self.gap_length,
            'end_length': len(self.end_buffer),
            'total_size': self.buffer_size,
            'cursor_pos': self.gap_index
        }

class SimpleTextEditor:
    """A simple text editor using gap buffer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Gap Buffer Text Editor")
        self.root.geometry("800x600")
        
        # Initialize gap buffer
        self.gap_buffer = GapBuffer()
        
        # Create GUI
        self.create_widgets()
        
        # Bind keyboard events
        self.bind_events()
        
        # Update display
        self.update_display()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", command=self.show_edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Buffer Stats", command=self.show_buffer_stats)
        
        # Main text area
        self.text_area = tk.Text(self.root, wrap=tk.WORD, undo=False)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)
    
    def show_edit_menu(self):
        """Show edit menu (placeholder)"""
        pass
    
    def bind_events(self):
        """Bind keyboard and mouse events"""
        self.text_area.bind('<Key>', self.on_key_press)
        self.text_area.bind('<Button-1>', self.on_click)
        self.text_area.bind('<KeyRelease>', self.on_key_release)
    
    def on_key_press(self, event):
        """Handle key press events"""
        if event.keysym == 'BackSpace':
            self.gap_buffer.delete()
            self.update_display()
            return 'break'
        elif event.keysym == 'Delete':
            self.gap_buffer.delete_forward()
            self.update_display()
            return 'break'
        elif event.keysym == 'Left':
            self.gap_buffer.move_cursor_left()
            self.update_display()
            return 'break'
        elif event.keysym == 'Right':
            self.gap_buffer.move_cursor_right()
            self.update_display()
            return 'break'
        elif event.keysym == 'Home':
            self.gap_buffer.move_cursor_to(0)
            self.update_display()
            return 'break'
        elif event.keysym == 'End':
            self.gap_buffer.move_cursor_to(len(self.gap_buffer.get_text()))
            self.update_display()
            return 'break'
        elif len(event.char) == 1:
            # Regular character
            self.gap_buffer.insert(event.char)
            self.update_display()
            return 'break'
    
    def on_click(self, event):
        """Handle mouse clicks to set cursor position"""
        # Get character index from click position
        index = self.text_area.index(f"@{event.x},{event.y}")
        char_index = int(float(index))
        self.gap_buffer.move_cursor_to(char_index)
        self.update_display()
    
    def on_key_release(self, event):
        """Handle key release events"""
        self.update_status()
    
    def update_display(self):
        """Update the text display"""
        # Get text from gap buffer
        text = self.gap_buffer.get_text()
        
        # Update text area
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, text)
        
        # Set cursor position
        cursor_pos = self.gap_buffer.get_cursor_position()
        self.text_area.mark_set(tk.INSERT, f"1.{cursor_pos}")
        
        # Update status
        self.update_status()
    
    def update_status(self):
        """Update status bar"""
        text = self.gap_buffer.get_text()
        cursor_pos = self.gap_buffer.get_cursor_position()
        stats = self.gap_buffer.get_stats()
        
        status_text = f"Cursor: {cursor_pos} | Length: {len(text)} | Gap: {stats['gap_length']}"
        self.status_bar.config(text=status_text)
    
    def new_file(self):
        """Create a new file"""
        self.gap_buffer = GapBuffer()
        self.update_display()
        self.status_bar.config(text="New file created")
    
    def open_file(self):
        """Open a file"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Open File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.gap_buffer = GapBuffer(content)
                self.update_display()
                self.status_bar.config(text=f"Opened: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def save_file(self):
        """Save the current file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                title="Save File",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                content = self.gap_buffer.get_text()
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.status_bar.config(text=f"Saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def cut_text(self):
        """Cut selected text (placeholder)"""
        messagebox.showinfo("Info", "Cut functionality not implemented yet")
    
    def copy_text(self):
        """Copy selected text (placeholder)"""
        messagebox.showinfo("Info", "Copy functionality not implemented yet")
    
    def paste_text(self):
        """Paste text (placeholder)"""
        messagebox.showinfo("Info", "Paste functionality not implemented yet")
    
    def show_buffer_stats(self):
        """Show gap buffer statistics"""
        stats = self.gap_buffer.get_stats()
        stats_text = f"""Gap Buffer Statistics:
        
Start Buffer Length: {stats['start_length']}
Gap Length: {stats['gap_length']}
End Buffer Length: {stats['end_length']}
Total Buffer Size: {stats['total_size']}
Cursor Position: {stats['cursor_pos']}
Text Length: {len(self.gap_buffer.get_text())}"""
        
        messagebox.showinfo("Buffer Statistics", stats_text)

def main():
    """Main function to run the text editor"""
    root = tk.Tk()
    editor = SimpleTextEditor(root)
    
    # Add some sample text
    sample_text = "Welcome to the Gap Buffer Text Editor!\n\nThis editor demonstrates how the gap buffer data structure works.\n\nTry typing, deleting, and moving the cursor around to see the gap buffer in action.\n\nUse the View menu to see buffer statistics."
    
    for char in sample_text:
        editor.gap_buffer.insert(char)
    editor.update_display()
    
    root.mainloop()

if __name__ == "__main__":
    main()
