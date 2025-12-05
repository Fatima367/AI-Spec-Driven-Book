// book_frontend/src/services/selection_service.ts

type SelectionChangeListener = (selectedText: string | null) => void;

class SelectionService {
  private listeners: SelectionChangeListener[] = [];
  private currentSelection: string | null = null;

  constructor() {
    if (typeof window !== 'undefined') { // Ensure this runs only in browser environment
      document.addEventListener('mouseup', this.handleSelectionChange);
      document.addEventListener('keyup', this.handleSelectionChange);
    }
  }

  private handleSelectionChange = () => {
    const selection = window.getSelection();
    let newSelectionText: string | null = null;

    if (selection && selection.toString().trim().length > 0) {
      newSelectionText = selection.toString().trim();
    }

    if (newSelectionText !== this.currentSelection) {
      this.currentSelection = newSelectionText;
      this.notifyListeners();
    }
  };

  private notifyListeners = () => {
    this.listeners.forEach(listener => listener(this.currentSelection));
  };

  public addSelectionChangeListener(listener: SelectionChangeListener): () => void {
    this.listeners.push(listener);
    // Return an unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  public getSelectedText(): string | null {
    return this.currentSelection;
  }

  // Cleanup for when the service is no longer needed (e.g., component unmount)
  public destroy() {
    if (typeof window !== 'undefined') {
      document.removeEventListener('mouseup', this.handleSelectionChange);
      document.removeEventListener('keyup', this.handleSelectionChange);
    }
    this.listeners = [];
  }
}

// Export a singleton instance of the service
export const selectionService = new SelectionService();
