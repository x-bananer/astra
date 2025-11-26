import "./button.css";

const Button = ({ children, size='', variant = "primary", active, className = "", ...props }) => {
    const classes = [
        "button",
        `button--${variant}`,
        `button--${size}`,
        active ? "button--active" : "",
        className
    ].join(" ").trim();
    
    return (
        <button className={classes} {...props}>
            {children}
        </button>
    );
};

export default Button;