import { selectionService } from '../selection_service';

describe('SelectionService', () => {
  let addEventListenerSpy: jest.SpyInstance;
  let removeEventListenerSpy: jest.SpyInstance;

  beforeAll(() => {
    // Mock window and document objects for JSDOM environment
    Object.defineProperty(window, 'getSelection', {
      value: jest.fn(() => ({
        toString: jest.fn(() => ''),
        removeAllRanges: jest.fn(),
        addRange: jest.fn(),
      })),
      writable: true,
    });
    addEventListenerSpy = jest.spyOn(document, 'addEventListener');
    removeEventListenerSpy = jest.spyOn(document, 'removeEventListener');
  });

  afterEach(() => {
    selectionService.destroy(); // Clean up listeners after each test
    jest.clearAllMocks();
  });

  it('should initialize and add event listeners', () => {
    new SelectionService(); // Re-initialize to check listeners
    expect(addEventListenerSpy).toHaveBeenCalledWith('mouseup', expect.any(Function));
    expect(addEventListenerSpy).toHaveBeenCalledWith('keyup', expect.any(Function));
  });

  it('should return null when no text is selected', () => {
    const selection = window.getSelection();
    (selection.toString as jest.Mock).mockReturnValue('');
    
    // Manually trigger the event listener
    const mouseupEvent = new Event('mouseup');
    document.dispatchEvent(mouseupEvent);

    expect(selectionService.getSelectedText()).toBeNull();
  });

  it('should update selected text when text is selected', () => {
    const selection = window.getSelection();
    (selection.toString as jest.Mock).mockReturnValue('test selection');
    
    // Manually trigger the event listener
    const mouseupEvent = new Event('mouseup');
    document.dispatchEvent(mouseupEvent);

    expect(selectionService.getSelectedText()).toBe('test selection');
  });

  it('should notify listeners when selection changes', () => {
    const listener = jest.fn();
    selectionService.addSelectionChangeListener(listener);

    const selection = window.getSelection();
    (selection.toString as jest.Mock).mockReturnValue('first selection');
    document.dispatchEvent(new Event('mouseup'));
    expect(listener).toHaveBeenCalledWith('first selection');

    (selection.toString as jest.Mock).mockReturnValue('second selection');
    document.dispatchEvent(new Event('mouseup'));
    expect(listener).toHaveBeenCalledWith('second selection');

    expect(listener).toHaveBeenCalledTimes(2); // Initial call + second change
  });

  it('should not notify listeners if selection does not change', () => {
    const listener = jest.fn();
    selectionService.addSelectionChangeListener(listener);

    const selection = window.getSelection();
    (selection.toString as jest.Mock).mockReturnValue('same selection');
    document.dispatchEvent(new Event('mouseup'));
    expect(listener).toHaveBeenCalledWith('same selection');

    document.dispatchEvent(new Event('mouseup')); // Trigger again with same text
    expect(listener).toHaveBeenCalledTimes(1);
  });

  it('should remove event listeners on destroy', () => {
    const service = new SelectionService();
    service.destroy();
    expect(removeEventListenerSpy).toHaveBeenCalledWith('mouseup', expect.any(Function));
    expect(removeEventListenerSpy).toHaveBeenCalledWith('keyup', expect.any(Function));
  });

  it('should unsubscribe listeners correctly', () => {
    const listener1 = jest.fn();
    const listener2 = jest.fn();

    const unsubscribe1 = selectionService.addSelectionChangeListener(listener1);
    selectionService.addSelectionChangeListener(listener2);

    const selection = window.getSelection();
    (selection.toString as jest.Mock).mockReturnValue('some text');
    document.dispatchEvent(new Event('mouseup'));
    expect(listener1).toHaveBeenCalledTimes(1);
    expect(listener2).toHaveBeenCalledTimes(1);

    unsubscribe1(); // Unsubscribe listener1

    (selection.toString as jest.Mock).mockReturnValue('new text');
    document.dispatchEvent(new Event('mouseup'));
    expect(listener1).toHaveBeenCalledTimes(1); // Should not have been called again
    expect(listener2).toHaveBeenCalledTimes(2); // Should have been called again
  });
});
