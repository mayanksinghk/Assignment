import Exceptions.EmptyLinkedList1;

import java.lang.*;
import java.util.*;

// IMPLEMENTING GENERAL TREE USING BINARY TREE

public class RoutingMapTree {
    Exchange Root = new Exchange(0);

    // Constructor to set the Root node to 0;  CHECKED
    RoutingMapTree() {
        Root.Number = 0;
    }

    // Finds the Exchange with Id same as number given to us we have to give Exchange E the Root of the Subtree or the tree else null; CHECKED
    public Exchange FindExchange(int number, Exchange E) {
        if (E != null) {
            if (E.Number == number) {
                return E;
            } else {
                Exchange c = FindExchange(number, E.LeftChild);
                if (c == null)
                    return FindExchange(number, E.RightChild);
                else
                    return c;
            }
        } else {
            return null;
        }
    }

    //Add Child to Node A and Makes it the parent of Node B. Duplicate Node not allowed. Parent must be present in the Tree; CHECKED
    public String addExchange(int a, int b) {
        Exchange B = new Exchange(b);
        Exchange A = new Exchange(a);
        if (FindExchange(a, Root) != null) {
            A = FindExchange(a, Root);
        }
        if (FindExchange(b, Root) != null) {
            B = FindExchange(b, Root);
        }

        if (FindExchange(B.Number, Root) == null && FindExchange(A.Number, Root) != null) {
            if (A.LeftChild == null) {
                A.LeftChild = B;
                B.Parent = A;
            } else {
                Exchange temp = A.LeftChild;
                while (temp.RightChild != null) {
                    temp = temp.RightChild;
                }
                temp.RightChild = B;
                B.Parent = temp;
            }
            return "";
        }
        if (FindExchange(A.Number, Root) == null) {
            return "Parent Node Missing";
        }
        return "";

    }

    //Deleting an Mobile in the tree
    public void DeleteMobilePhone(MobilePhone a, Exchange b) {
        try {
            b.SetOfMobile.Delete(a);
            DeleteMobilePhone(a, b.LeftChild);
            DeleteMobilePhone(a, b.RightChild);
        } catch (Exception E) {
        }
    }

    //Inserting Element in a particular place and updating in the whole tree
    public String InsertMobile(MobilePhone a) {
        Exchange temp = FindExchange(a.BaseStation.Number, Root);
        if (a.BaseStation.IsLeaf()) {
            while (temp != Root) {
                temp.SetOfMobile.Insert(a);
                temp = temp.getParent();
            }
            temp.SetOfMobile.Insert(a);
            return "";
        } else {
            return "Mobile can be Inserted at the base station only";
        }
    }

    //Switch on the mobile phone if Mobile present at given Node else if Mobile is registered at some other node and is Switched On then it gives error but inf the Mobile is Switched
    // off then it deletes the Mobile from that Node and Inserts it on the Node given
    public String switchOnMobile(int a, int b) throws EmptyLinkedList1 {
        Exchange temp = FindExchange(b, Root);
        MobilePhone Mobile = SearchMobileInTree(a);
        MobilePhone tempMobile = new MobilePhone(a);
        if (Mobile == null) {                                        // Checking Mobile in the Root
            if (temp == null) {                                      // checking if the Node Exist or not
                return "Cannot find the Node";
            } else {
                if (temp.IsLeaf() == true) {                       // Checking if Node is the Leaf Node or not
                    tempMobile.BaseStation = temp;
                    while (temp != null) {                         // Inserting element in the Base Station and Updating the subsequent parent
                        temp.SetOfMobile.Insert(tempMobile);
                        temp = temp.getParent();
                    }
                    return "";
                } else {                                           // Error if Node is not Leaf Node
                    return "Mobile can be inserted in the Base Station Only";
                }
            }
        } else {
            if (temp == null) {                                      // Checking if the Node exist or not
                return "Node not present";
            } else {
                if (temp.IsLeaf() == true) {
                    if (Mobile.State == false) {                    // check if mobile is switched off
                        if (Mobile.BaseStation != temp) {
                            Mobile.BaseStation.SetOfMobile.Delete(Mobile);
                            Exchange toUpdate = Mobile.BaseStation;
                            while (toUpdate != null) {              // Deleting the Mobile from the tree and from all the parents of the node
                                toUpdate.SetOfMobile.Delete(Mobile);
                                toUpdate.getParent();
                            }
                            Mobile.BaseStation = temp;
                            while (temp != null) {                  // Adding the element in the Node and updating the information on all the successive node
                                temp.SetOfMobile.Insert(Mobile);
                                temp = temp.getParent();
                            }
                            return "";
                        } else {
                            Mobile.State = true;
                            while (temp != null) {                 // Updating the state of the Mobile Phone on all the parents and the Node to true
                                temp.SetOfMobile.FindMobilePhone(a).State = true;
                                temp = temp.getParent();
                            }
                            return "";
                        }
                    } else {
                        return "Mobile Phone is Registered to other Base Station";
                    }
                } else {
                    return "Mobile can be inserted in the Base Station Only";
                }

            }
        }

    }

    public void showAllMobile(Exchange E) {
        if (E != null) {
            showAllMobile(E.LeftChild);
            showAllMobile(E.RightChild);
            System.out.println(E.SetOfMobile.Show());

        }
    }

    //Find and Return Mobile Phone if not present it returns null  CHECKED
    public MobilePhone SearchMobileInTree(int A) {
        MobilePhone temp = new MobilePhone(A);
        if (Root.SetOfMobile != null) {
            try {
                if (Root.SetOfMobile.IsMember(temp)) {
                    Node temp2 = Root.SetOfMobile.list.getHead();
                    while (temp2 != null) {
                        if (((MobilePhone) temp2.object).Number == A) {
                            return ((MobilePhone) temp2.object);
                        }
                        temp2 = temp2.next;
                    }
                } else {
                    return null;
                }
            } catch (EmptyLinkedList1 Ee) {
                return null;
            }
        }
        return null;
    }

    // SwitchOff the given Mobile and update in all over the tree
    public void switchOff(MobilePhone A, Exchange E) {
        if (E == null) {

        } else {
            try {
                if (E.SetOfMobile.IsMember(A)) {
                    A.State = false;
                } else {
                    switchOff(A, E.RightChild);
                    switchOff(A, E.LeftChild);
                }
            } catch (Exception e) {

            }
        }
    }

    // Gives Nth Child of the Node with Id a if b > (no. of Children of node a) returns null. Returns null in case their is no Node with Id equals to a;   CHECKED
    public Exchange queryNthChild(int a, int b) {
        Exchange tempExchange = FindExchange(a, Root);
        try {
            int result = 0;
            if (result == b) {
                return tempExchange.LeftChild;
            } else {
                tempExchange = tempExchange.LeftChild;
                while (result != b) {
                    if (tempExchange == null) {
                        return null;
                    }
                    tempExchange = tempExchange.RightChild;
                    result = result + 1;
                }
                return tempExchange;
            }
        } catch (Exception E) {
            return null;
        }
    }

    // Returns the String of MobilePhone in the given set;   CHECKED
    public String queryMobilePhoneSet(int a) {

        String temps = "";
        Exchange tempExchange = FindExchange(a, Root);
        if (tempExchange != null) {
            if (tempExchange.SetOfMobile != null) {
                temps = tempExchange.SetOfMobile.Show();
            } else {
                temps = "Set is Empty";
            }
        } else {
            temps = "Set is Empty";
        }
        return temps;
    }

    // Returns the Base Station with which mobile phone is registered if not found returns null  CHECKED
    public Exchange findPhone(MobilePhone a) {
        MobilePhone M = SearchMobileInTree(a.Number);
        if (M == null) {
            return null;
        } else {
            return M.BaseStation;
        }
    }

    //Returns the Lowest router or in sense we can say that it returns the first common parent in the tree  CHECKED
    public Exchange lowestRouter(Exchange a, Exchange b) {
        a = FindExchange(a.Number, Root);
        b = FindExchange(b.Number, Root);
        if(a == null || b == null){
            return null;
        }else{
            if(a.Number == b.Number){
                return a;
            }else{
                ExchangeList E1 = new ExchangeList();

                Exchange tempb = b;
                while(tempb != Root){
                    E1.InsertEnd(tempb);
                    tempb = tempb.getParent();
                }
                E1.InsertEnd(tempb);

                Exchange tempa = a;
                while(E1.Search(tempa) == false ){
                    tempa = tempa.getParent();
                }

                return tempa;
            }
        }
    }

    //Returns the List of Exchanges that gives the path from one phone to the other phone  CHECKED
    public ExchangeList routeCall(MobilePhone a, MobilePhone b) {
        ExchangeList returnlist = new ExchangeList();
        if (a == null || b == null) {
            return null;
        } else {
            Exchange llowestRouter = lowestRouter(a.BaseStation, b.BaseStation);
            if (llowestRouter == a.BaseStation) {
                returnlist.Insert(a.BaseStation);
            } else {
                Exchange tempa = a.BaseStation;
                Exchange tempb = b.BaseStation;
                ExchangeList templist = new ExchangeList();
                Node tempnode = null;
                while (tempa.Number != llowestRouter.Number) {
                    returnlist.InsertEnd(tempa);
                    tempa = tempa.getParent();
                }

                returnlist.InsertEnd(llowestRouter);

                while (tempb != llowestRouter) {
                    templist.Insert(tempb);
                    tempb = tempb.getParent();
                }
                tempnode = templist.list.head;
                while (tempnode != null) {
                    returnlist.InsertEnd(((Exchange) tempnode.object));
                    tempnode = tempnode.next;
                }

            }
            return returnlist;
        }
    }

    //Moves the Mobile a from its Base station to new Base Station
    public String movePhone(MobilePhone a, Exchange b) {
        if (FindExchange(b.Number, Root) == null) {              //Checking if Node with identifier B exist or not
            return "Cannot Find the Exchange with identifier";
        } else {
            if (SearchMobileInTree(a.Number) == null) {          // Checking if Mobile Phone with identifier a exists or not
                return "Cannot find the given Mobile identifier";
            } else {
                MobilePhone temp = new MobilePhone(a.Number);
                temp.BaseStation = b;
                if (a.BaseStation == b) {
                    return "";
                } else {
                    DeleteMobilePhone(a, Root);
                    return InsertMobile(temp);
                }
            }
        }
    }

    public String performAction(String actionMessage) {

        String s = "";
        String[] words = actionMessage.split(" ");
        if (words[0].equals("addExchange")) {
            int a = Integer.parseInt(words[1]);
            int b = Integer.parseInt(words[2]);
            addExchange(a, b);
            return s;
        } else {
            if (words[0].equals("switchOnMobile")) {
                int a = Integer.parseInt(words[1]);
                int b = Integer.parseInt(words[2]);
                try {
                    s = switchOnMobile(a, b);
                } catch (EmptyLinkedList1 E) {
                    s = "Error : Empty Linked List";
                }
                return s;
            } else {
                if (words[0].equals("switchOffMobile")) {
                    int a = Integer.parseInt(words[1]);
                    MobilePhone temp = SearchMobileInTree(a);
                    if (temp == null) {
                        s = "Error Mobile Phone not found";
                    } else {
                        switchOff(temp, Root);
                    }
                    return s;
                } else {
                    if (words[0].equals("queryNthChild")) {
                        int a = Integer.parseInt(words[1]);
                        int b = Integer.parseInt(words[2]);
                        Exchange resultExchange = queryNthChild(a, b);
                        if (resultExchange == null) {
                            s = "Error bth child does not Exists";
                        } else {
                            s = actionMessage + ": " + resultExchange.Number;
                        }
                        return s;
                    } else {
                        if (words[0].equals("queryMobilePhoneSet")) {
                            int a = Integer.parseInt(words[1]);
                            s = queryMobilePhoneSet(a);
                            String[] tempo = s.split(" ");
                            String news = "";
                            int len = tempo.length;
                            int i = len - 1;
                            while (i > -1) {
                                news = news + tempo[i] + ", ";
                                i = i - 1;
                            }
                            news = news.substring(0, news.length() - 1);
                            s = news;
                            s = actionMessage + ": " + s;
                            len = s.length();
                            s = s.substring(0, len - 1);
                            return s;
                        } else {
                            if (words[0].equals("findPhone")) {
                                int a = Integer.parseInt(words[1]);
                                MobilePhone aa = SearchMobileInTree(a);
                                s = "queryFindPhone " + words[1] + ": ";
                                if (aa == null) {
                                    return "queryFindPhone " + words[1] + ": Error - No mobile phone with identifier " + words[1] + " found in the network";
                                } else {
                                    s = s + aa.BaseStation.Number ;
                                    return s;
                                }
                            } else {
                                if (words[0].equals("lowestRouter")) {
                                    int a = Integer.parseInt(words[1]);
                                    int b = Integer.parseInt(words[2]);
                                    s = "queryLowestRouter " + words[1] + " " + words[2] + ": ";
                                    Exchange atemp = FindExchange(a, Root);
                                    Exchange btemp = FindExchange(b, Root);
                                    Exchange E = lowestRouter(atemp, btemp);

                                    s = s + E.Number;
                                    return s;
                                } else {
                                    if (words[0].equals("findCallPath")) {
                                        int a = Integer.parseInt(words[1]);
                                        int b = Integer.parseInt(words[2]);
                                        MobilePhone atemp = SearchMobileInTree(a);
                                        MobilePhone btemp = SearchMobileInTree(b);
                                        if (atemp.State == false) {
                                            s = "queryFindCallPath " + words[1] + " " + words[2] + ": " + "Error - Mobile phone with identifier " + words[1] + " is currently switched off";
                                        } else {
                                            if (btemp.State == false) {
                                                s = "queryFindCallPath " + words[1] + " " + words[2] + ": " + "Error - Mobile phone with identifier " + words[2] + " is currently switched off";
                                            } else {
                                                if (routeCall(atemp, btemp) == null) {
                                                    s = "queryFindCallPath " + words[1] + " " + words[2] + ": " + "Error ";
                                                } else {
                                                    s = "queryFindCallPath " + words[1] + " " + words[2] + ": " + routeCall(atemp, btemp).list.ShowElement();
                                                }
                                            }
                                        }
                                        return s;
                                    } else {
                                        if (words[0].equals("movePhone")) {
                                            int a = Integer.parseInt(words[1]);
                                            int b = Integer.parseInt(words[2]);
                                            s = words[0] + " : ";
                                            MobilePhone atemp = SearchMobileInTree(a);
                                            Exchange btemp = FindExchange(b, Root);
                                            s = movePhone(atemp, btemp);
                                            return s;
                                        }
                                        return s;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
