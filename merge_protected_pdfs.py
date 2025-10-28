import os
from pypdf import PdfReader, PdfWriter
from getpass import getpass

def merge_protected_pdfs(folder_path, output_file):
    # Ask for the common password (hidden input)
    password = getpass("Enter the PDF password: ")

    # Prepare PDF writer
    writer = PdfWriter()

    # Get all PDF files in the folder, sorted alphabetically
    pdf_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    )

    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    print(f"Found {len(pdf_files)} PDF files. Processing...")

    for pdf_name in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_name)
        try:
            reader = PdfReader(pdf_path)

            # Try to decrypt using the provided password
            if reader.is_encrypted:
                if reader.decrypt(password) == 0:
                    print(f"❌ Incorrect password for {pdf_name}. Skipping.")
                    continue

            for page in reader.pages:
                writer.add_page(page)

            print(f"✅ Added: {pdf_name}")

        except Exception as e:
            print(f"⚠️ Error reading {pdf_name}: {e}")

    # Write the combined PDF
    output_path = os.path.join(folder_path, output_file)
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"\n🎉 Merged PDF saved as: {output_path}")


if __name__ == "__main__":
    folder = input("Enter the folder path with PDFs: ").strip()
    output = input("Enter the output PDF file name (e.g., merged.pdf): ").strip()

    if not output.lower().endswith(".pdf"):
        output += ".pdf"

    merge_protected_pdfs(folder, output)

