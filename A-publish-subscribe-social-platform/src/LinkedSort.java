public class LinkedSort {
    public class SortNode {
        TextSort text = new TextSort();
        SortNode next;

        public SortNode(String Text, int Time) {
            text.text = Text;
            text.time = Time;
            next = null;
        }

    }

    SortNode head = null;

    public void Insert(String text, int time) {
        SortNode node = new SortNode(text, time);
        if (head == null) {
            head = node;
        } else {
            node.next = head;
            head = node;
        }
    }

    public int Length() {
        SortNode node = head;
        int count = 0;

        while (node != null) {
            count = count + 1;
            node = node.next;
        }
        return count;
    }

}
