public class InvertedPageIndex {
    MySet<PageEntry> pageEntry = new MySet<>();
    MyHashTable UniversalTable = new MyHashTable();

    void addPage(PageEntry p){
        pageEntry.AddElement(p);
    }

    MySet<PageEntry> getPagesWhichContainWord(String str){
        MySet temp = new MySet();

        return  temp;
    }
}
