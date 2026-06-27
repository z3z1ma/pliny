type IconActionButtonProps = {
  label: string;
  disabled?: boolean;
  onActivate: () => void;
};

export function IconActionButton({
  label,
  disabled = false,
  onActivate,
}: IconActionButtonProps) {
  return (
    <button
      type="button"
      aria-label={label}
      disabled={disabled}
      onClick={onActivate}
    >
      <span aria-hidden="true">⋯</span>
    </button>
  );
}
