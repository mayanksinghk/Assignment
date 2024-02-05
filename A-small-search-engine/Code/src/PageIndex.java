import org.w3c.dom.ls.LSException;

public class PageIndex {

    Position P ;
    String str ;
    MyLinkedList<WordEntry> ListOfWord = new MyLinkedList();
    private Node temp = ListOfWord.head;
    private int a = 0;

    void addPositionForWord(String str, Position p){
        //System.out.println("1");
        WordEntry tt = new WordEntry(str);
        tt.AddPosition(p);

        Node temp1 = temp;
        //System.out.println(temp);
        if(temp == null){
            a = 1;
        }else{
            a = 0;
        }

        //System.out.println(temp);
    	while(temp1 != null && !((WordEntry) temp1.d).str.equals(str)){
    	        ((WordEntry) temp1.d).AddPosition(p);
    	         temp1 = temp1.next;
        }
        if(temp1 != null || a == 1){
            if(a == 1){
                //System.out.println(tt.str + "  " + p.P.PageName + " " + p.WordIndex);
                ListOfWord.InsertStart(tt);
                temp = ListOfWord.head;
            }else{
                //System.out.println(tt.str + "  " + p.P.PageName + " " + p.WordIndex);
                ((WordEntry) temp1.d).AddPosition(p);
            }
        }else{
    	    //System.out.println(tt.str + "  " + p.P.PageName + " " + p.WordIndex);
    	    ListOfWord.InsertStart(tt);
        }
    }

    public void Show(){
        Node tempt = ListOfWord.head;
        Node temp2 = tempt;
        while(tempt != null){
            System.out.print(((WordEntry) tempt.d).str + " " );
            ((WordEntry) tempt.d).list.list.Show();
            temp2 = tempt;
            tempt = tempt.next;
        }
    }

}
