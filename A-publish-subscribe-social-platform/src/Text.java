public class Text {
    public int TextId ;
    public String TextString;
    public int TimeStamp;
    public int State;
    public int ReplyId;

    //Constructor to assign values like TextId, TextString and TimeStamp to the object
    public Text(int TextId, String TextString, int TimeStamp, int state){
        this.TextId = TextId;
        this.TextString = TextString;
        this.TimeStamp = TimeStamp;
        this.State = state;
        ReplyId = -1;
    }

}
