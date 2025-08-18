export default function Button({ children, ...props }) {
  return (
    <button
      {...props}
      style={{
        padding: "8px 16px",
        background: "#007bff",
        border: "none",
        borderRadius: "4px",
        color: "#fff",
        cursor: "pointer"
      }}
    >
      {children}
    </button>
  );
}
