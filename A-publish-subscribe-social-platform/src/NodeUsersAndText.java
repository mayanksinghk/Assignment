
public class NodeUsersAndText {

    int textid;
    int pid;
    String text;
    NodeUsersAndText next ;

    public NodeUsersAndText(int Pid, int Textid, String Text){
        this.textid = Textid;
        this.pid = Pid;
        this.text = Text;
        next = null;
    }
}
