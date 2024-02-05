public class SearchEngine {

    public ListOfUsers UserList = new ListOfUsers();
    public LinkedListOfTextAndUsers TextList = new LinkedListOfTextAndUsers();


    //first inserts the user with given user id then subscribe option is performed
    public void Subscribe(String Time, String Uid, String Pid, String st) {
        int time = Integer.parseInt(Time);
        int uid = Integer.parseInt(Uid);
        int pid = Integer.parseInt(Pid);
        User temp1 = new User(uid, time);
        User temp2 = new User(pid, time);
        UserList.Insert(temp1);
        UserList.Insert(temp2);


        Subscribe(time, uid, pid, st);
    }

    private void Subscribe(int time, int uid, int pid, String st) {
        UserNode temp1 = UserList.Search(uid);
        System.out.println(st);
        temp1.data.Subscribe(time, pid);
    }

    //Unsubscribe the given users
    public void Unsubscribe(String Time, String Uid, String Pid, String st) {
        int time = Integer.parseInt(Time);
        int uid = Integer.parseInt(Uid);
        int pid = Integer.parseInt(Pid);

        Unsubscribe(time, uid, pid, st);
    }

    private void Unsubscribe(int time, int uid, int pid, String st) {
        UserNode temp1 = UserList.Search(uid);
        UserNode temp2 = UserList.Search(pid);
        if (temp1 == null || temp2 == null) {
            System.out.println("uid " + uid + " has not subscribed to pid " + pid);
        } else {
            String string = temp1.data.Unsubscribe(pid, time);
            if (string.length() != 0) {
                System.out.println(string);
            } else {
                System.out.println(st);
            }
        }
    }

    //publishing New Article by a publisher with given UId and given Text  and Text Id
    public void NewPublish(String Time, String Uid, String text, String Tid) {
        int time = Integer.parseInt(Time);
        int uid = Integer.parseInt(Uid);
        int tid = Integer.parseInt(Tid);

        NewPublish(time, uid, text, tid);
    }

    //State = 1 means new state
    private void NewPublish(int time, int uid, String text, int tid) {
        UserNode node = UserList.Search(uid);
        if (node == null) {
            System.out.println("Publisher not found");
        } else {
            //System.out.println(TextList.Insert(uid, tid));
            if (TextList.Insert(uid, tid, text)) {
                node.data.TextList.Insert(time, text, tid, 1);
            } else {
                System.out.println("Can't publish with tid " + tid);
            }
        }
    }

    //Reposting an article the article was originally posted by some other publisher
    public void Repost(String Time, String Uid, String Ptid, String Tid, String st) {
        int time = Integer.parseInt(Time);
        int uid = Integer.parseInt(Uid);
        int tid = Integer.parseInt(Tid);
        int ptid = Integer.parseInt(Ptid);

        Repost(time, uid, ptid, tid, st);
    }

    //State = 2 means that the post is reposted
    private void Repost(int time, int uid, int ptid, int tid, String st) {
        UserNode node = UserList.Search(uid);
        NodeUsersAndText node1 = TextList.Search(ptid);
        NodeUsersAndText node2 = TextList.Search(tid);
        if (node != null) {
            if (node1 == null) {
                System.out.println("No text with ptid " + ptid);
            } else {
                if (node2 != null) {
                    System.out.println("Can't publish with tid " + tid);
                } else {
                    System.out.println(st);
                    node.data.TextList.Insert(time, node1.text, tid, 2);
                    TextList.Insert(uid, tid, node1.text);
                }
            }
        } else {
            System.out.println("Publisher Not Present with uid" + uid);
        }
    }

    //Replying to a Post of another publisher
    public void Reply(String Time, String Uid, String Pid, String text, String Tid) {
        int time = Integer.parseInt(Time);
        int uid = Integer.parseInt(Uid);
        int pid = Integer.parseInt(Pid);
        int tid = Integer.parseInt(Tid);

        Reply(time, uid, pid, text, tid);
    }

    //State = 3 represents the reply text
    private void Reply(int time, int uid, int pid, String text, int tid) {
        UserNode node = UserList.Search(uid);
        NodeUsersAndText node1 = TextList.Search(pid);
        NodeUsersAndText node2 = TextList.Search(tid);
        if (node == null) {
            System.out.println("Publisher Referring to not presente");
        } else {
            if (node1 == null) {
                System.out.println("Text with given Id not present");
            } else {
                if (node2 != null) {
                    System.out.println("Given text Id cannot be assigned as it is already present");
                } else {
                    node.data.TextList.Insert(time, text, tid, 3);
                    TextList.Insert(uid, tid, text);
                    node.data.TextList.SetReplyId(time, pid);
                }
            }
        }
    }

    //Shows the list of  all the text that a user can see based on his subscription
    public void Read(String Time, String Uid, String st) {
        int time = Integer.parseInt(Time);
        int uid = Integer.parseInt(Uid);

        Read(time, uid, st);
    }

    private void Read(int time, int uid, String st) {
        UserNode user = UserList.Search(uid);
        int flag = 1;
        if (user == null) {
            System.out.println("Given user is does not exists");
        } else {

            LinkedSort sort = new LinkedSort();

            String string = ",[";
            /*NodeText text1 = user.data.TextList.head;
            while(text1 != null){
                if(user.data.lasttime <= text1.text.TimeStamp && text1.text.TimeStamp < time){
                    //string = string + text1.text.TextString + ",";
                    flag = 0;
                }
                text1 = text1.next;
            }*/
            Node temp = user.data.Sublist.head;
            while (temp != null) {
                if (temp.status == true && temp.time < time) {
                    UserNode node = UserList.Search(temp.data);
                    NodeText textnode = node.data.TextList.head;
                    while (textnode != null) {
                        if (user.data.lasttime <= textnode.text.TimeStamp && textnode.text.TimeStamp < time && temp.time <= textnode.text.TimeStamp) { //put equal to show the answers as if time is discrete else remove = in last statement
                            //string = string + textnode.text.TextString + ",";
                            sort.Insert(textnode.text.TextString, textnode.text.TimeStamp);
                            flag = 0;
                        }
                        textnode = textnode.next;
                    }
                }
                temp = temp.next;
            }
            if (flag == 1) {
                System.out.println("No text available for uid " + uid);
            } else {
                QuickSort sort1 = new QuickSort();
                sort1.sort(sort);
                TextSort[] SortedText = sort1.input;
                for (int i = 0; i < SortedText.length; i++) {
                    string = string + SortedText[i].text + ",";
                }
                System.out.println(st + string.substring(0, string.length() - 1) + "]");
            }
            user.data.lasttime = time;
        }
    }

    //Main function used for all queries and all the interface
    public void performAction(String st) {
        String st1 = st.replace("(", ",");
        String string = st1.replace(")", "");
        String[] word = string.split(",");

        //To Subscribe a user
        if (word[0].toLowerCase().equals("subscribe")) {
            Subscribe(word[1], word[2], word[3], st);
        }

        //To unsubscribe a user
        if (word[0].toLowerCase().equals("unsubscribe")) {
            Unsubscribe(word[1], word[2], word[3], st);
        }

        //To read the text from the publishers
        if (word[0].toLowerCase().equals("read")) {
            Read(word[1], word[2], st);
        }

        //To publish NEW text from the publisher
        if (word[0].toLowerCase().equals("publish") && word[3].toLowerCase().equals("new")) {
            System.out.println(st);
            NewPublish(word[1], word[2], word[4], word[5]);
        } else {
            //To Repost a text published initially by another publishers
            if (word[0].toLowerCase().equals("publish") && word[3].toLowerCase().equals("repost")) {
                Repost(word[1], word[2], word[4], word[5], st);
            }

            //To reply to a text published by a user
            if (word[0].toLowerCase().equals("publish") && word[3].toLowerCase().equals("reply")) {
                System.out.println(st);
                Reply(word[1], word[2], word[4], word[5], word[6]);
            }
        }

    }
}
