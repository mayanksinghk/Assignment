public class LinkedListText {
    NodeText head ;

    //Inserts a new element in the list;
    public void Insert(int Time ,String Text, int tid, int state){
        Text data = new Text(tid, Text, Time, state);
        NodeText temp = new NodeText(data);
        NodeText node = Search(tid);
        if(node == null){
            if(head == null){
                head = temp;
            }else{
                temp.next = head ;
                head = temp;
            }
        }
    }

    //Search and return a node with given text id if not found return null
    public NodeText Search(int id){
        NodeText node = head;
        while(node != null){
            if(node.text.TextId == id){
                return node;
            }
            node = node.next;
        }
        return null;
    }

    public int GetReplyId(int id){
        NodeText node = Search(id);
        if(node == null){
            return -1;
        }
        return node.text.ReplyId;
    }

    public void SetReplyId(int tid, int pid){
        NodeText node = Search(tid);
        if(node != null){
            node.text.ReplyId = pid;
        }
    }

}
