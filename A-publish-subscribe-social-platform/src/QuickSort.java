public class QuickSort {
    public TextSort input[];
    private int length;

    public void sort(LinkedSort numbers) {
        if (numbers == null || numbers.Length() == 0) {
            return;
        }
        ConvertToArray(numbers);
        length = input.length;
        quicksort(0, length - 1);

    }

    private void quicksort(int low, int high) {
        int i = low;
        int j = high;

        TextSort pivot = input[low + (high - low) / 2];

        while (i < j) {
            while (input[i].time < pivot.time) {
                i = i + 1;
            }
            while (input[j].time > pivot.time) {
                j = j - 1;
            }
            if (i <= j) {
                swap(i, j);
                i = i + 1;
                j = j - 1;
            }

        }

        if (low < j) {
            quicksort(low, j);
        }
        if (i < high) {
            quicksort(i, high);
        }
    }

    private void swap(int i, int j) {
        TextSort temp = input[i];
        input[i] = input[j];
        input[j] = temp;
    }

    private void ConvertToArray(LinkedSort some) {
        length = some.Length();
        TextSort[] replacement = new TextSort[length];

        int i = 0;
        LinkedSort.SortNode temp = some.head;
        while (temp != null) {
            replacement[i] = temp.text;
            i = i + 1;
            temp = temp.next;
        }
        input = replacement;
    }
}
