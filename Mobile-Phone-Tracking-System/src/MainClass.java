import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.security.PrivilegedExceptionAction;

public class MainClass
{
    public static void main ( String args [])
    {
        BufferedReader br = null;
        RoutingMapTree r = new RoutingMapTree();

        try {
            String actionString;
            br = new BufferedReader(new FileReader("action.txt"));

            while ((actionString = br.readLine()) != null) {
                String s = r.performAction(actionString);
                System.out.print(s);
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
       /* Exchange E1 = new Exchange(1);
        Exchange E2 = new Exchange(2);
        Exchange E3 = new Exchange(3);
        Exchange E4 = new Exchange(4);
        Exchange E5 = new Exchange(5);
        r.addExchange(0,E1.Number);
        r.addExchange(2,0);
        r.addExchange(3,0);
        r.addExchange(4,1);
        r.addExchange(5,1);
        System.out.println(E1.getParent().Number);
        Exchange E = r.lowestRouter(E2, E1);
        System.out.println();*/
       /*System.out.println(" --------------------");
       Exchange E1 = r.FindExchange(7, r.Root);
       Exchange E2 = r.FindExchange(4, r.Root);
       Exchange E = r.lowestRouter(E1, E2);
       System.out.println(E.Number);*/
    }
}
