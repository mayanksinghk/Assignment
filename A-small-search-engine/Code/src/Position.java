public class Position {
    public PageEntry P;
    public int WordIndex;

    //Constructor to initialise the value
    public Position(PageEntry p, int wordIndex) {
        P = p;
        WordIndex = wordIndex;
    }

    public PageEntry getPageEntry() {
        return P;
    }

    public int getWordIndex() {
        return WordIndex;
    }
}
