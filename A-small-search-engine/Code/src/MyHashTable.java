import java.util.LinkedList;

public class MyHashTable {

    MySet<WordEntry>[] SetOfWord = new MySet[200];

    private int getHashIndex(String str){
        int ascii  = str.charAt(0);
        int asci = str.charAt(str.length()-1);
        int i = (ascii + asci )%200;
        return i;
    }

    void addPositionsForWord(WordEntry w){
        int pos = getHashIndex(w.str);
        //System.out.println(SetOfWord[pos]);
        if(SetOfWord[pos] == null){
            //System.out.println("SetOfWord[" + pos +"] is null " + w.str);
            MySet<WordEntry> temp = new MySet<>();
            temp.AddElement(w);
            SetOfWord[pos] = temp;
        }else{
            //System.out.println("1111 " + w.str);
            int a = 0;
            Node<WordEntry>  mayank = SetOfWord[pos].list.head;
            Node<WordEntry> store = null;
            while(mayank != null){
                if(mayank.d.str.equals(w.str)){
                  a = 1;
                  store = mayank;
                }
                mayank = mayank.next;
            }
            if(a!= 0 ){
                //System.out.print( w.str + "__________  " );
                Node templisthead = store.d.list.list.head;
                while(templisthead != null){
                    //System.out.print(((Position) templisthead.d).WordIndex + "@" + ((Position) templisthead.d).P.PageName + " ");
                    templisthead = templisthead.next;
                }
                //System.out.println(((Position) w.list.list.head.d).WordIndex + "@" + ((Position) w.list.list.head.d).P.PageName + " ");
                //System.out.println(" ");
                store.d.list = store.d.list.Union(w.list);
            }else{
                SetOfWord[pos].AddElement(w);
                //System.out.println(w.str + " " + ((Position) w.list.list.head.d).P.PageName);
            }

            //Checking if the word is already in the hashtable or not;
            //System.out.println("SetOfWord[" + pos +"] is not null " + w.str);
            //Node temp =  SetOfWord[pos].list.head;
            //System.out.println(temp);

            //System.out.println(((WordEntry) temp.d).str);
            //Node temp1 = temp;
            //System.out.println( ((WordEntry) temp.d).str + " " + w.str );
            //System.out.println(!((WordEntry) temp.d).str.equals(w.str));
            //while ( !(((WordEntry) temp.d).str.equals(w.str))  && temp != null){
              //  temp1 = temp;
              //  temp = temp.next;
            //}
            //System.out.println(((WordEntry) temp.d).str);
            //If not found then it is added in the table else not
           /* if(temp == null){
                SetOfWord[pos].AddElement(w);
            }else{

                // if entry is found then merging the entries in the word entry
                ((WordEntry) temp.d).list = ((WordEntry) temp.d).list.Union(w.list);
//                ((WordEntry) temp1.d).list = ((WordEntry) temp1.d).list.Union(w.list);

            }*/
        }
    }

    public void show(){
        int i = 0;
        while(i<200){
            if(SetOfWord[i] != null){
                Node temp = SetOfWord[i].list.head;
                while(temp != null){
                    System.out.print(((WordEntry) temp.d).str + " " );
                    temp = temp.next;
                }
                System.out.print(i);
                System.out.println(" ");
            }
            /*if(SetOfWord[i] != null){
                System.out.println(((WordEntry) SetOfWord[i].list.head.d).str);
            }*/
            i = i + 1;
        }
    }

    public WordEntry Search(String str){
        int pos = getHashIndex(str);
        WordEntry tempword = new WordEntry(str);
        if(SetOfWord[pos] == null){
            return null;
        }
        Node<WordEntry> temp = SetOfWord[pos].list.head;
        //System.out.println(str + " " + temp.d.str);
        while(temp != null){
            if(temp.d.str.equals(str)){
                tempword = temp.d;
                return tempword;
            }
            temp = temp.next;
        }
        if(temp == null){
            return null;
        }else{
            return tempword;
        }
    }
}
