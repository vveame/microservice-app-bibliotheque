package prete_service.exception;

public class ActiveLoanException extends RuntimeException {
    public ActiveLoanException(String message) {
        super(message);
    }
}