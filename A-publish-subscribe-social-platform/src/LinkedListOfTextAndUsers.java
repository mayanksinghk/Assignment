public class LinkedListOfTextAndUsers {
    NodeUsersAndText head;

    public Boolean Insert(int pid, int textid, String text) {
        NodeUsersAndText node = new NodeUsersAndText(pid, textid, text);
        NodeUsersAndText temp = Search(textid);
         //System.out.println(textid + ", " + temp);
        if (temp == null) {
            if (head == null) {
                head = node;
            } else {
                node.next = head;
                head = node;
            }
            return true;
        }
        return false;
    }

    public NodeUsersAndText Search(int textid) {
        NodeUsersAndText node = head;
        while (node != null) {
            if (node.textid == textid) {
                return node;
            }
            node = node.next;
        }
        return node;
    }

    public int GetPid(int textid){
        NodeUsersAndText node = Search(textid);
        return node.pid;
    }

}
