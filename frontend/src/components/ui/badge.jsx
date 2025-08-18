export default function Badge({ children, ...props }) {
  return (
    <span
      {...props}
      style={{
        display: "inline-block",
        padding: "2px 8px",
        fontSize: "12px",
        fontWeight: "500",
        borderRadius: "8px",
        backgroundColor: "#eee",
        color: "#333"
      }}
    >
      {children}
    </span>
  );
}
