package another;

/**
 * Created by amala on 25/11/2016.
 */
public class Type1Model extends MyBaseTypeModel {
    private String outerName;
    private internalclass ic;

    public String getOuterName() {
        return outerName;
    }

    public void setOuterName(String outerName) {
        this.outerName = outerName;
    }

    public internalclass getIc() {
        return ic;
    }

    public void setIc(internalclass ic) {
        this.ic = ic;
    }
}

class internalclass{
    private String innerName;
}
