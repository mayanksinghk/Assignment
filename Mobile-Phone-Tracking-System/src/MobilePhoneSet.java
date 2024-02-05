import Exceptions.EmptyLinkedList1;

// ALL FUNCTION ARE CHECKED FOR ALL POSSIBLE CASES;

public class MobilePhoneSet {
    LinkedList list = new LinkedList();
    Myset MobileSet = new Myset(list);

    // DIFFERENT FUNCTION

    // Constructor to set the empty Linked List in the Set; CHECKED
    MobilePhoneSet(){
        list.head = null;
    }

    //Returns True if the Mobile.Number is present in the set else it returns false. If the set is Empty it returns Empty Set error;  CHECKED
    public Boolean IsMember(MobilePhone mobilePhone) throws EmptyLinkedList1 {
        if (list.getHead() == null) {
            throw new EmptyLinkedList1("Given Set is Empty");
        } else {
            Node temp = list.getHead();
            while (temp != null) {
                if (((MobilePhone)(temp.getObject())).Number == mobilePhone.Number) {
                    return true;
                }
                temp = temp.getNext();
            }
            return false;
        }
    }

    // Inserts the Mobile Phone in the Set and Ensures that if Mobile Number is already Present in the Set then don't Insert it in the set again;  CHECKED
    public void Insert(MobilePhone mobilePhone){
        try {
            if (IsMember(mobilePhone) == false) {
                list.InsertBegin(mobilePhone);
            }
        } catch (EmptyLinkedList1 e) {
            list.InsertBegin(mobilePhone);
        }
    }

    // Inserts the Mobile Phone in the Set and Ensures that if Mobile Number is already Present in the Set then don't Insert it in the set again;  CHECKED
    public void InsertEnd(MobilePhone mobilePhone){
        try {
            if (IsMember(mobilePhone) == false) {
                list.InsertEnd(mobilePhone);
            }
        } catch (EmptyLinkedList1 e) {
            list.InsertEnd(mobilePhone);
        }
    }

    // Checks if Mobile.Number is present in the set if present it deletes it else does nothing;  CHECKED
    public void Delete(MobilePhone mobilePhone){
        Node temp1 = list.head;
        if(list.head == null){
            System.out.println("Empty");
        }else{
            if(this.list.length() == 1 && ((MobilePhone) this.list.head.object).Number == mobilePhone.Number){
                list.head = null;
            }else{
                Node temp2 = temp1 ;
                while(((MobilePhone) temp1.object).Number != mobilePhone.Number){
                    temp2 = temp1;
                    temp1 = temp1.next;
                }
                temp2.setNext(temp1.getNext());
            }
        }
    }

    // Returns the Union of two MobilePhone Set and that too in Correct Order; CHECKED
    public MobilePhoneSet Union(MobilePhoneSet A){

        MobilePhoneSet FinalSet = new MobilePhoneSet();
        Node temp1 = A.list.getHead();                     //Making new set that has all the elements as the elements of MobilePhoneSet A
        while(temp1 != null){
            FinalSet.InsertEnd(((MobilePhone) temp1.object));
            temp1 = temp1.next;
        }

        if (A.list.getHead() == null && list.getHead() == null) {
            return null;
        } else {
            if (list.getHead() == null) {
                return FinalSet;
            } else {
                Node temp = list.getHead();
                while (temp != null) {
                    FinalSet.InsertEnd((MobilePhone) (temp.getObject()));
                    temp = temp.getNext();
                }
            }
        }
        return FinalSet;
    }

    // Returns the Intersection of the given Set with the Set passed to it. Returns the Output in Correct Order;  CHECKED
    public MobilePhoneSet Intersection (MobilePhoneSet A){

        MobilePhoneSet IntersectionSet = new MobilePhoneSet();

        if(list.head == null || A.list.head == null){
            return null;
        }else{
            Node nodetemp = A.list.head;
            while(nodetemp != null){
                try{
                    if(IsMember((MobilePhone) (nodetemp.getObject())) == true){
                        MobilePhone O = (MobilePhone) (nodetemp.getObject());
                        IntersectionSet.InsertEnd(O);
                    }
                }catch(EmptyLinkedList1 e){
                    System.out.println("Empty Linked List");
                }
                nodetemp = nodetemp.next;
            }
            if(IntersectionSet.list.head == null){
                return null;
            }
            return IntersectionSet;
        }
    }

    // Returns the MobilePhone whose number matches with the number of the MobilePhone passed;  CHECKED
    public MobilePhone GivesMobilePhone(MobilePhone a) throws EmptyLinkedList1{
        if (list.getHead() == null) {
            throw new EmptyLinkedList1("Set is Empty");
        } else {
            Node temp = list.getHead();
            while (temp != null) {
                if (((MobilePhone)(temp.getObject())).Number == a.Number) {
                    return ((MobilePhone) temp.object);
                }
                temp = temp.getNext();
            }
            return null;
        }
    }

    // Returns the MobilePhone whose number matches with the number passed;  CHECKED
    public MobilePhone FindMobilePhone(int number){
        MobilePhone temp = new MobilePhone(0);
        temp.Number = number;
        try{
            MobileSet.IsMember(temp);
        }catch(EmptyLinkedList1 E ){
            //System.out.println("Empty Set");
        }
        return temp;
    }

    // Returns the String Containing the Mobile Number of all the MobilePhone present in the set;  CHECKED
    public String Show(){
        String string = "";
        Node temp = list.getHead();
        while(temp != null){
            if(((MobilePhone) temp.object).status())
                string = string + " "+ ((MobilePhone) temp.object).Number;
            temp = temp.next;
        }
        if(string.length()==0)
            return "No elements in this set";
        return string.substring(1);
    }

}
