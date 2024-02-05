import Exceptions.EmptyLinkedList1;
import Exceptions.NotPresentInSet;

public class Myset {
    LinkedList list;

    Myset(LinkedList l) {
        list = l;
    }

    Myset() {
        list.setHead(null);
    }

    public Boolean IsEmpty() {
        return null == list.head;
    }

    public Boolean IsMember(Object o) throws EmptyLinkedList1 {
        if (list.getHead() == null) {
            throw new EmptyLinkedList1("Linked is Empty");
        } else {
            Node temp = list.getHead();
            while (temp.getNext() != null) {
                if (temp.getObject() == o) {
                    return true;
                }
                temp = temp.getNext();
            }
            if (temp.getObject() == o) {
                return true;
            } else {
                return false;
            }
        }
    }

    public void Insert(Object o) {
        try {
            if (IsMember(o) == false) {
                list.InsertBegin(o);
            }
        } catch (EmptyLinkedList1 e) {
            list.InsertBegin(o);
        }
    }

    public void Delete(Object o) throws NotPresentInSet {
        try {
            if (IsMember(o) == false) {
                throw new NotPresentInSet("Element not present in the set");
            } else {
                list.DeleteObject(o);
            }
        } catch (EmptyLinkedList1 e) {
            System.out.println("Set is Empty");
        }
    }

    public Myset Union(Myset a) {
        Myset FinalSet = a;
        if (a.list.getHead() == null && list.getHead() == null) {
            return null;
        } else {
            if (list.getHead() == null) {
                return a;
            } else {
                Node temp = list.getHead();
                while (temp.getNext() != null) {
                    FinalSet.Insert(temp.getObject());
                    temp = temp.getNext();
                }
                FinalSet.Insert(temp.getObject());
            }
        }
        return FinalSet;
    }

    public Myset Intersection(Myset a){
        LinkedList newList = new LinkedList();
        if(list.head == null || a.list.head == null){
            return null;
        }else{
            Node nodetemp = a.list.head;
                while(nodetemp.getNext() != null){
                    try{
                        if(IsMember(nodetemp.getObject()) == true){
                            Object O = nodetemp.getObject();
                            newList.InsertBegin(O);
                        }
                    }catch(EmptyLinkedList1 e){
                        System.out.println("Empty Linked List");
                    }
                    nodetemp = nodetemp.next;
                }

            try{
                if(IsMember(nodetemp.getObject()) == true){
                    Object O = nodetemp.getObject();
                    newList.InsertBegin(O);
                }
            }catch(EmptyLinkedList1 e){
                System.out.println("Empty Linked List");
            }
                Myset IntersectionSet = new Myset(newList);
                return IntersectionSet;
        }
    }

    public int LengthOfSet(){
        int a = 0;
        System.out.println(this.list);
        a = list.length();
        return a;
    }

    public void show() {
        list.ShowElement();
    }

}
