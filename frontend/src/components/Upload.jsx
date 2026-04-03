function Upload({ isDragging, onDragOver, onDragLeave, onDrop, onSelect }) {
  return (
    <label
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
      className={`relative block cursor-pointer border-2 p-10 text-center transition ${
        isDragging ? "border-sheild-red bg-sheild-red/10" : "border-sheild-red/50 bg-black/30"
      }`}
    >
      <input
        type="file"
        className="hidden"
        accept="image/*,video/mp4"
        onChange={(e) => onSelect(e.target.files?.[0])}
      />
      <span className="font-display text-4xl text-sheild-paper">Drop Evidence Here</span>
      <p className="mt-2 font-mono text-xs text-sheild-paper/70">JPG, PNG, WEBP, MP4 (max 50MB)</p>
    </label>
  );
}

export default Upload;
