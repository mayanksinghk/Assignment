public class Exchange {
    int Number;
    Exchange LeftChild = null;
    Exchange RightChild = null;
    MobilePhoneSet SetOfMobile = new MobilePhoneSet();
    Exchange Parent = null;

    // DIFFERENT FUNCTION

    // Constructor of the class that sets the number;
    public Exchange(int number) {
        Number = number;
    }

    //Returns true for root otherwise false;
    public Boolean IsRoot(){
        if(Parent == null){
            return true;
        }else{
            return false;
        }
    }

    // Returns true for Leaf for Case of General tree otherwise false;
    public Boolean IsLeaf(){
        if(LeftChild == null){
            return true;
        }
        else{
            return false;
        }
    }

    // Returns the parent of the Node;
    public Exchange getParent(){
        Exchange temp = this.Parent;

        if(this.Parent != null) {
            if (temp.RightChild == this) {
                return temp.getParent();
            } else {
                return temp;
            }
        }else{
            return null;
        }
    }

    // Sets the parent of the Node;
    public void SetParent(Exchange parent){
        Parent = parent;
    }

    //Inserts Element in the Resident Set
    public void InsertInResidentSet(MobilePhone A){

    }
    // Returns the ResidentSet of the Node;    // To be corrected;
    public MobilePhoneSet residentSet(){
        if(this.LeftChild != null){
            SetOfMobile = this.SetOfMobile.Union(this.LeftChild.residentSet());
            Exchange temp = this.RightChild;
            while(temp != null){
                SetOfMobile = this.SetOfMobile.Union(temp.residentSet());
                temp = temp.RightChild;
            }
            return SetOfMobile;
        }
        return null;
    }

    // Add the Child Node to the given Node;   // Doesn't Decide if it is left child or Right Child
    public void AddChild(Exchange Child){
        Child.SetParent(this);
    }


}
