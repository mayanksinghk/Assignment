import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class SearchEngine {
    public InvertedPageIndex InvertedPage = new InvertedPageIndex();


    public void AddPage(String pageName) {
        PageEntry page = new PageEntry(pageName);

        String temp = "";
        String Adress1 = "./src/webpages/" + pageName;

        //Reading the given document and Storing it in a Long String
        BufferedReader br = null;
        try {
            String actionString;
            br = new BufferedReader(new FileReader(Adress1));

            while ((actionString = br.readLine()) != null) {
                temp = temp + " "+actionString;
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

        //words is an array that stores the individual words in an Array
        String[] words = temp.split("\\s++|\\{|}|<|>|\\(|\\)|\\.|,|;|'|\"|\\?|#|!|-|:|=| |\n|\t");

        //Creating an position object to store the data for individual word
        int i = 1;
        Position pos = new Position(page, i);
        MyLinkedList<String> WordList = Convert(words);
        Node<String> tempwords = WordList.head;



        //Reading word from the Linked list of words and storing it in the pageIndex
        while(tempwords  != null ){
            pos.WordIndex = i;
            if(tempwords.d.equals("stacks") || tempwords.d.equals("structures")|| tempwords.d.equals("applications")){
                tempwords.d = tempwords.d.substring(0, tempwords.d.length()-1);
            }
            if(!Check(tempwords.d)){
                page.maya.addPositionForWord(tempwords.d, pos);
                WordEntry wordEntry = new WordEntry(tempwords.d);
                wordEntry.AddPosition(pos);
                InvertedPage.UniversalTable.addPositionsForWord(wordEntry);
                //System.out.print(tempwords.d + " ");
            }
            i = i +1;
            tempwords = tempwords.next;
        }
        InvertedPage.pageEntry.AddElement(page);
    }

    public Boolean Check(String str){
        Boolean temp = false;
        if(str.equals("a") || str.equals("an") || str.equals("the") || str.equals("they") || str.equals("these") || str.equals("this") || str.equals("for") ||  str.equals("is") ||  str.equals("are") || str.equals("was") || str.equals("of") || str.equals("or") || str.equals("and") || str.equals("does") || str.equals("will") || str.equals("whose")){
            temp = true;
        }
        return temp;
    }

    private MyLinkedList Convert(String[] arr){
        MyLinkedList<String> WordList = new MyLinkedList<>();
        int i = 0;
        while(i<arr.length){
            if(arr[i].length() >=1){
                WordList.InsertEnd(arr[i].toLowerCase());
            }
            i = i+1;
        }
        return WordList;
    }


    public void performAction(String str ){
        String[] word = str.split(" ");
        if(word[0].equals("addPage")){
            AddPage(word[1]);
            //InvertedPage.UniversalTable.show();
            //System.out.println("##########");
        }
        if(word[0].equals("queryFindPagesWhichContainWord")){
            String st1 = word[1].toLowerCase();
            WordEntry wordd = InvertedPage.UniversalTable.Search(st1);
            MySet<String> Pages = new MySet<>();
            if(wordd == null){
                System.out.println("No webpage contain word " + st1 );
            }else {
                Node<Position> tempmay =  wordd.list.list.head;

                while (tempmay != null) {
                    Pages.AddElement( tempmay.d.P.PageName);
                    tempmay = tempmay.next;
                }

                Node temp2 = Pages.list.head;
                String string = "";
                while (temp2 != null) {
                    //System.out.println(temp2.d + "#######");
                    string =  string + ", " + temp2.d;
                    temp2 = temp2.next;
                }
                System.out.println(string.substring(2));
            }
        }
        if(word[0].equals("queryFindPositionsOfWordInAPage")){
            String st1 = word[1].toLowerCase();
            String st2 = word[2];

            String store = "";
            WordEntry wordd = InvertedPage.UniversalTable.Search(st1);
            if(wordd == null){
                System.out.println("Webpage " + st2 +" does not contain the word " + st1);
            }else{
                int a = 0;
                Node<PageEntry> tempnode = InvertedPage.pageEntry.list.head;
                while(tempnode != null){
                    if(tempnode.d.PageName.equals(st2)){
                        a = 1;
                    }
                    tempnode = tempnode.next;
                }
                if(a == 0){
                    System.out.println("Page Not Found");
                }else {
                    Node<Position> tempword = wordd.list.list.head;
                    while(tempword != null){
                        if(tempword.d.P.PageName.equals(st2)){
                            store = store + ", " + tempword.d.WordIndex;
                        }
                        tempword = tempword.next;
                    }
                }
            }
        }
        //InvertedPage.pageEntry.ShowElement();
    }


}
