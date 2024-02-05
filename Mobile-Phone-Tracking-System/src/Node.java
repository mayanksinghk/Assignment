
public class Node {
    Object object;
    Node next;

    Node(Object o){
        object = o;
        next = null;
    }
    Node(){
        object = null;
        next = null;
    }

    public Object getObject() {
        return object;
    }

    public void setObject(Object object) {
        this.object = object;
    }

    public Node getNext() {
        return next;
    }

    public void setNext(Node next) {
        this.next = next;
    }


}
