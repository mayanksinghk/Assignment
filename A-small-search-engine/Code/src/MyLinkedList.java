public class MyLinkedList<Datatype> {
    Node head = null;

    MyLinkedList(){
        head = null;
    }

    //Inserting Element at the end of the list;
    public void InsertEnd(Datatype data){
        Node node = new Node(data);

        if(head == null){
            head = node;
        }else{
            Node temp = head;
            while(temp.next != null){
                temp = temp.next;
            }
            temp.next = node;
        }
    }

    //Inserting Element at the start of the list;
    public void InsertStart(Datatype data){
        Node node = new Node(data);
        if (head == null) {
            head = node;
        }else{
            Node temp = head;
            head = node;
            node.next = temp;
        }
    }

    //Returns the length of the list;
    public int length(){
        int a = 0;
        if(head != null){
            Node temp = head;
            while(temp != null){
                a = a +1;
                temp = temp.next;
            }
        }
        return a ;
    }

    //Delete the Element with the given data;
    public void DeleteElement(Datatype data){
        if(this.length() == 1 && this.head.d == data){
            head = null;
        }else{
            Node temp = head;
            Node sectemp = temp;
            while(temp.d != data){
                sectemp = temp;
                temp = temp.next;
            }
            sectemp.next = temp.next;
        }
    }

    //Deletes the element from the start of the list;
    public void DeleteStart(){
        if(this.head != null){
            if(this.length() == 1){
                head = null;
            }else{
                head = head.next;
            }
        }
    }

    public void Show(){
        Node<Datatype> temp = head;
        while(temp != null){
            System.out.println(temp.d);
            temp = temp.next;
        }
    }

}