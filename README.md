To help others understand and use your **Scholar PDF Downloader**, a strong GitHub README should be clear, professional, and explain exactly how to get the program running on a Windows laptop. 

Here is an extended description you can copy and paste into your `README.md` file.

---

# Scholar PDF Downloader Pro (Windows)

A Python-based desktop application designed for researchers to perform **bulk, automated downloads** of academic papers from Google Scholar. This tool features a user-friendly graphical interface (GUI) and a smart history-tracking system to ensure you never download the same paper twice.

## ## Key Features

* **Fresh Search Technology:** Pulls the latest indexed papers (both historical and recent) directly from Google Scholar.
* **Duplicate Prevention:** Maintains a `download_record.txt` file in your save directory. If a paper has been downloaded before, the program automatically skips it.
* **Smart Naming:** Automatically names every PDF file using its **actual paper title** while stripping illegal characters to ensure they open on Windows without errors.
* **Year Filtering:** Target specific publication windows (e.g., 2023–2026) to find the most relevant current research.
* **Full Download Assurance:** Uses streaming data chunks to ensure PDF files are downloaded completely, preventing "corrupted file" errors.
* **Control Interface:** Includes **Start**, **Pause**, and **Resume** buttons to manage long-running bulk download tasks.
* **Direct Save:** Saves files individually to your chosen location (Laptop or Google Drive) without zipping or compressing.

---

## ## Requirements

To run this on your Windows laptop, you will need:
* **Python 3.x**
* **Libraries:** `scholarly`, `requests`, `beautifulsoup4`

Install the dependencies via Command Prompt:
```bash
pip install scholarly requests beautifulsoup4
```

---

## ## How to Use

1.  **Run the Script:** Double-click the `.py` file to open the window.
2.  **Enter Topic:** Type your research topic (e.g., "Machine Learning in Healthcare").
3.  **Set Years:** Define the publication range (e.g., From 2022 To 2026).
4.  **Set Count:** Choose how many **new** papers you want to fetch.
5.  **Select Folder:** After clicking **Start**, a Windows folder picker will appear. Choose your destination (works perfectly with Google Drive for Desktop sync folders).
6.  **Monitor Progress:** Use the status bar to see real-time download updates and the "Total Papers in History" counter.

---

## ## Technical Specifications

* **GUI Framework:** Tkinter (Native Windows)
* **Search Engine:** Scholarly (Google Scholar Wrapper)
* **Download Method:** Requests (Stream-based)
* **Anti-Bot Protection:** Includes built-in headers and time delays to mimic human browsing and prevent IP blocking.

---

## ## Disclaimer
This tool is intended for personal research purposes only. Please respect the Terms of Service of Google Scholar and the individual publishers of the academic papers. Use a VPN if performing extremely large bulk downloads to avoid temporary IP rate-limiting.
