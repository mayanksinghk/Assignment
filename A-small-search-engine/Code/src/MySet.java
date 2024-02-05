public class MySet<Datatype> {
    Datatype datatype;
    MyLinkedList<Datatype> list = new MyLinkedList<>();

    MySet(Datatype GetData){
        datatype = GetData;
    }

    public MySet() {
        datatype = null;
    }

    //Returns true if the element is found in the list else returns false;
    Boolean search(Datatype data){
        Node temp = list.head;
        if(temp == null){
            return false;
        }else {
            while ( temp != null && temp.d != data) {
                temp = temp.next;
            }
            if (temp != null) {
                return true;
            } else {
                return false;
            }
        }
    }

    // Add the element in the list if the element is already present it doesn't do anything;
    void AddElement(Datatype data){
        if(!search(data)){
            list.InsertStart(data);
        }
    }

    //Returns the union of two  sets
    public MySet<Datatype> Union(MySet<Datatype> A){
        MySet<Datatype> temp = new MySet<>();
        Node temp1 = list.head;

        //copying the item in new set
        while(temp1 != null){
            temp.AddElement(((Datatype) temp1.d));
            temp1 = temp1.next;
        }

        temp1 = A.list.head;
        //copying the item in new set
        while(temp1 != null){
            temp.AddElement(((Datatype) temp1.d));
            temp1 = temp1.next;
        }
        return temp;
    }

    //Returns the Intersection of two sets
    public MySet<Datatype> Intersection(MySet<Datatype> A){
        MySet<Datatype> temp = new MySet<>();

        Node temp1 = A.list.head;
        while(temp1 != null){
            if(search(((Datatype) temp1.d))){
                temp.AddElement(((Datatype) temp1.d));
            }
            temp1 = temp1.next;
        }

        if(temp.list.length() <1){
            return null;
        }
        return temp;
    }

    //Show function in Myset to print all the element in the set
    public void ShowElement(){
        Node temp = list.head;
        while(temp != null){
            System.out.print(" " + ((Datatype) temp.d));
            temp = temp.next;
        }
    }
}
