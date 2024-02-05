public class User {
    LinkedList Sublist = new LinkedList();
    LinkedListText TextList = new LinkedListText();
    int UId;
    int timeStamp;
    int lasttime;

    //Constructor to initialise the user
    public User(int Uid, int TimeStamp) {
        this.UId = Uid;
        this.timeStamp = TimeStamp;
        this.lasttime = -1;
    }

    //Subscribe to User with given UId
    public void Subscribe(int time, int Uid) {
        Sublist.Insert(Uid, time);
        Sublist.Subscribe(Uid, time);
    }

    //Unsubscribe to a given User
    public String Unsubscribe(int Uid, int time) {
        String s = Sublist.Unsubscribe(Uid, time, UId);
        return s;
    }

}
