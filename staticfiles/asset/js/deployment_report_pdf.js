

window.onload = function () {
  document.getElementById("download").addEventListener("click", () => {
    const element = this.document.getElementById("report");
    // console.log(invoice);
    // console.log(window);
    var opt = {
      margin: 2,
      filename: "myfile.pdf",
      image: { type: "jpeg", quality: 1 },
      html2canvas: { scale: 6 },
      jsPDF: {
        unit: "mm",
        format: "a4",
        orientation: "landscape",
        putOnlyUsedFonts: true,
        compress: true,
      },
    };

    html2pdf().set(opt).from(element).save();
  });
};
