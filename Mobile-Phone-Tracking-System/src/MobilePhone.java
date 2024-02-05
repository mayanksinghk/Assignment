import Exceptions.MobilePhoneOffException;
import java.lang.*;

// ALL FUNCTION ARE CHECKED FOR ALL POSSIBLE CASES;

public class MobilePhone {
    int Number ;
    Exchange BaseStation = null;
    Boolean State;

    //DIFFERENT FUNCTION

    //Constructor to initialise the MobilePhone Object with the given number and its state is Initialised to true;  CHECKED
    MobilePhone(int number){
        Number = number;
        State = true;
    }

    // Returns the Status of the MobilePhone Object;  CHECKED
    public Boolean status(){
        return State;
    }

    // Returns the Number of the MobilePhone Object;  CHECKED
    public int number(){
        return Number;
    }

    // Sets the State of the Mobile Phone to true that is Mobile Phone is Switched On;  CHECKED
    public void switchOn(){
        State = true;
    }

    // Sets the State of the Mobile Phone to false that is Mobile Phone is Switched Off;  CHECKED
    public void switchOff(){
        State = false;
    }

    //Returns the Base Station with which the mobile phone is registered;  CHECKED
    public Exchange location() throws MobilePhoneOffException{
        if(State == true){
            return BaseStation;
        }else{
            throw new MobilePhoneOffException("The Mobile Phone is Switched Off");
        }
    }
}
