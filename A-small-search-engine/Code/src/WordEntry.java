public class WordEntry {
    public String str ;
    MySet<Position> list = new MySet<>();

    public WordEntry(String str) {
        this.str = str;
    }

    public void AddPosition(Position position){
        list.AddElement(position);
    }

    public void addPositions(MyLinkedList<Position> positions){
        Node temp = positions.head;
        
        while(temp != null){
            list.AddElement(((Position) temp.d));
            temp = temp.next;
        }
    }

    public MyLinkedList GetAllPositionsForThisWord(){
        return list.list;
    }

    public float getTermFrequency(String Word){
        float f = list.list.length();
        return f;
    }

    public void Show(){
        Node temp = list.list.head;
        while(temp != null){
            System.out.print("("+((Position) temp.d).P.PageName + " " + ((Position) temp.d).WordIndex + ")" + " ");
            temp = temp.next;
        }
    }

}
