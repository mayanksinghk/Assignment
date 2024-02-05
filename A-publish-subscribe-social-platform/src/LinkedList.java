public class LinkedList {
    Node head;

    //Inserts the new element in the beginning of the list;
    public void Insert(int datatype, int time) {

        Node t = Search(datatype);
        if (t == null) {
            if (head == null) {
                Node temp = new Node(datatype);
                temp.time = time;
                head = temp;
            } else {
                Node temp = new Node(datatype);
                temp.time = time;
                temp.next = head;
                head = temp;
            }
        }

    }

    //Searches for a particular integer in the list;
    public Node Search(int datatype) {
        Node temp = head;
        while (temp != null) {
            if (temp.data == datatype) {
                return temp;
            }
            temp = temp.next;
        }
        return temp;
    }

    //Subscribe to a particular user with given User Id at a given time
    public void Subscribe(int Uid, int time) {
        Node temp = Search(Uid);
        if (temp != null) {
            temp.status = true;
            temp.time = time;
        } else {
            System.out.println("Publisher not found ");
        }
    }

    //UnSubscribe to a particular user with given User Id at a given time
    public String Unsubscribe(int Uid, int time, int UId) {
        String st = "";
        Node temp = Search(Uid);
        if (temp != null) {
            if (temp.status == false) {
                st = "Uid " + UId + " has not subscribed to pid " + Uid;
            } else {
                temp.status = false;
                temp.time = time;
            }
        } else {
            st = "Publisher not found ";
        }
        return st;
    }
}
