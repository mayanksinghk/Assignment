public class ExchangeList {

    LinkedList list = new LinkedList();

    public void Insert(Exchange E) {
        list.InsertBegin(E);
    }

    public void DeleteEnd() {
        list.DeleteEnd();
    }

    public void DeleteObject(Exchange O) {
        Node temp = list.head;
        if (temp == null) {
            System.out.println("Empty List");
        } else {
            Node temp2 = temp;
            while (temp.object != O) {
                temp = temp.getNext();
                temp2 = temp;
            }
            temp2.setNext(temp.getNext());
        }
    }

    public int Length() {
        int a = 0;
        a = list.length();
        return a;
    }

    public void ShowElement() {
        list.ShowElement();
    }

    public void InsertEnd(Exchange O) {
        list.InsertEnd(O);
    }

    public boolean Search(Exchange E){
        Node Head = list.head;
        while(Head != null){
            if(((Exchange) Head.object).Number == E.Number){
                return true;
            }
            Head = Head.next;
        }
        return false;
    }

}
