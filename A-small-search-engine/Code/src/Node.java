public class Node<Datatype> {
    Datatype d;
    Node next;

    Node(){
        next = null;
    }

    Node(Datatype data){
        this.d = data;
        this.next = null;
    }
}
