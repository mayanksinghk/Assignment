import java.io.*;
import java.util.*;
public class PageEntry {
    String PageName;
    PageIndex maya = new PageIndex();

    public PageEntry(String str){
        PageName = str;
    }



}
/*    public PageEntry(String pageName) {
        PageName = pageName;
        String temp = null;
        String Adress1 = "./src/webpages/" + pageName;

        //Reading the given document and Storing it in a Long String
        BufferedReader br = null;
        try {
            String actionString;
            br = new BufferedReader(new FileReader(Adress1));

            while ((actionString = br.readLine()) != null) {
                temp = temp + actionString;
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
        int i = 0;
        PageEntry page = new PageEntry();
        page.PageName = pageName;
        Position pos = new Position(page, i);
        MyLinkedList<String> WordList = Convert(words);
        Node<String> tempwords = WordList.head;

        //Reading word from the array words and storing it in the pageIndex
        try{
            while(tempwords  != null ){
                pos.WordIndex = i+1;
                //System.out.println(pos.WordIndex);
                if(tempwords.d.equals("stacks") || tempwords.d.equals("structures")|| tempwords.d.equals("applications")){
                    tempwords.d = tempwords.d.substring(0, tempwords.d.length()-1);
                }
                if(!Check(tempwords.d)){
                    maya.addPositionForWord(tempwords.d, pos);

                }
                i = i+1;
                tempwords = tempwords.next;
            }
        }catch(Exception E){
           // System.out.println("Error");
        }
        //  maya.Show();
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
    }*/
