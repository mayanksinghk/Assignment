public class ListOfUsers {



    UserNode head ;

    //Search a particular User using its User Id
    public UserNode Search(int UId){
        UserNode temp = head;

        while(temp != null){
            if(temp.data.UId == UId){
                return temp;
            }
            temp = temp.next;
        }
        return temp;
    }

    //Inserting an element in the list and not allowing repeated User Id
    public void Insert(User user){
        UserNode temp = Search(user.UId);
        if(temp == null){
            UserNode node = new UserNode(user);
            if(head == null){
                head = node;
            }else{
                node.next = head;
                head = node;
            }
        }
    }

    //Show the details of the list of the all the users present in the list
    public void Show(){
        UserNode temp = head;
        //System.out.println(temp);
        while(temp != null){
            Node node = temp.data.Sublist.head;
            System.out.println(temp.data.UId);
            while(node != null){
                System.out.print(node.data + "-" + node.status + ", ");
                node = node.next;
            }
            System.out.println("");
            temp = temp.next;
        }
    }

    //show the List of the users stored in the list
    public void showusers(){
        UserNode node = head;
        while(node != null){
            System.out.print(node.data.UId + ", ");
            node = node.next;
        }
    }

}
