import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args){
        /*MySet<Integer> temp = new MySet<Integer>();
        temp.AddElement(34);
        temp.AddElement(35);
        temp.AddElement(36);
        temp.AddElement(34);
        temp.ShowElement();

        System.out.println(" ");

        MySet<Integer> temp1 = new MySet<Integer>();
        temp1.AddElement(344);
        temp1.AddElement(355);
        temp1.AddElement(366);
        temp1.AddElement(34);
        temp1.ShowElement();

        System.out.println(" ");

        MySet tempU = temp1.Intersection(temp);
        tempU.ShowElement();*/


        /*MyHashTable temp = new MyHashTable();
        WordEntry word = new WordEntry("hello");
        WordEntry word1 = new WordEntry("yello");
        WordEntry word2 = new WordEntry("hello");

        temp.addPositionsForWord(word);
        temp.addPositionsForWord(word1);
        temp.addPositionsForWord(word2);

        temp.show();*/

        //File file = new File("/webpages/references");

     // PageEntry temp = new PageEntry("stack_oracle");
        /*PageEntry page = new PageEntry();

        PageIndex temp = new PageIndex();
        Position pos1 = new Position(page, 1);
        Position pos2 = new Position(page, 1);
        Position pos3 = new Position(page, 1);
        temp.addPositionForWord("yoyo", pos1);
        temp.addPositionForWord("yoyo", pos2);
        temp.addPositionForWord("yoyoyo", pos3);
        temp.addPositionForWord("yoyoyoyoyo", pos1);
        temp.addPositionForWord("momomo", pos3);

        temp.Show();*/

       /* SearchEngine temp = new SearchEngine();
        //temp.SearchEngine("addPage stack_oracle");
        temp.SearchEngine("addPage stacklighting");
        temp.SearchEngine("addPage stack_oracle");
        temp.SearchEngine("queryFindPagesWhichContainWord residential");
        //temp.InvertedPage.UniversalTable.show();
       // temp.AddPage("stack_oracle");
   /*     for(int i = 0; i<200; i++ ){
            if(temp.InvertedPage.UniversalTable.SetOfWord[i] != null){
                System.out.println(temp.InvertedPage.UniversalTable.SetOfWord[i].list.head);
            }
        }*/

      /* MyHashTable table = new MyHashTable();
       WordEntry word1 = new WordEntry("mayank1");
       WordEntry word2 = new WordEntry("myyank2");
       WordEntry word3 = new WordEntry("mayank2");
       table.addPositionsForWord(word1);
        table.addPositionsForWord(word2);
        table.addPositionsForWord(word3);
       table.show();*/




        BufferedReader br = null;
        SearchEngine r = new SearchEngine();

        try {
            String actionString;
            br = new BufferedReader(new FileReader("actions.txt"));

            while ((actionString = br.readLine()) != null) {
                r.performAction(actionString);
               // System.out.print(s);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (br != null)br.close();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
        //r.InvertedPage.UniversalTable.show();
      //Node<PageEntry> temp = r.InvertedPage.pageEntry.list.head;
       /* while (temp != null){
            Node<WordEntry> temp2 = temp.d.maya.ListOfWord.head;
            while(temp2 != null){
                System.out.print(" " + temp2.d.str);
                temp2 = temp2.next;
            }
            System.out.println(" ");
            temp = temp.next;
        }*/
       //System.out.println(" 111111111111");
       //System.out.println(r.InvertedPage.UniversalTable.Search("c++").str);

    }
}
