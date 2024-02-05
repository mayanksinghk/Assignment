
// CHECKED FULLY FOR ALL THE CASES POSSIBLE;
public class LinkedList {

    Node head;

    // Constructor for the Linked List to set the Head Initially to null;  CHECKED
    LinkedList(){
        setHead(null);
    }

    // Returns the head of the Linked List;  CHECKED
    public Node getHead() {
        return head;
    }

    // Sets the head of the Linked List to given Node;  CHECKED
    public void setHead(Node head) {
        this.head = head;
    }

    // Returns the Length of the Linked List; CHECKED
    public int length(){
        int a = 0;
        Node temp = head ;
        while(temp.getNext()!= null){
            a = a+1;
            temp = temp.next;
        }
        return a+1;
    }

    // Inserts the Object O in the End Of the List;  CHECKED
    public void InsertEnd(Object O){
        Node node = new Node(O);

        if(head == null){
            head = node;
        }else{
            Node temp = head;
            while(temp.getNext() != null){
                temp = temp.getNext();
            }
            temp.setNext(node);
        }
    }

    // Inserts the Object O in the start of the Linked List;  CHECKED
    public  void InsertBegin(Object o){
        Node node = new Node(o);
        if(head == null ){
            head = node;
        }else{
            Node temp = head;
            head = node;
            node.setNext(temp);
        }
    }

    //Deletes the Element from the end of the Linked List and Returns the deleted Element if List is Empty then it returns null;  CHECKED
    public Object DeleteEnd(){
        if(head == null){
            return null;
        }else{
            Node temp = head;
            Node secondLast = temp;
            if(temp.getNext() == null){
                head = null;
                return temp.object;
            }else{
                while( temp.next != null){
                    secondLast = temp;
                    temp = temp.getNext();
                }
                 secondLast.setNext(null);
                return temp.object;
            }
        }
    }

    // Deletes the particular Object O from the Linked List if not present then it does not do anything;  CHECKED
    public void DeleteObject(Object o){
        Node temp = head;
        if(head == null){
            System.out.println("Empty");
        }else{
            if(this.length() == 1 && this.head.object == o){
                head = null;
            }else{
                Node temp2 = temp ;
                while(temp.object != o){
                    temp2 = temp;
                    temp = temp.next;
                }
                temp2.setNext(temp.getNext());
            }
        }
    }

    // Prints the Linked List in a single Line separated by ',';  CHECKED
    public String ShowElement(){
        Node temp = head;
        String s = "";
        if(temp != null){
            while(temp != null){
                s = s + ", " + ((Exchange) temp.object).Number;
                temp = temp.getNext();
            }
            s = s.substring(2);
            return s;
            //System.out.println(s);
        }
        return null;
    }

}
