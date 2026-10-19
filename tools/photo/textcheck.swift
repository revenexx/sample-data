// Finds lettering in product photos with Apple's Vision text recognition.
// The AI step sometimes prints made-up brand names on a product, which a
// public sample dataset must not carry. Prints one line per image:
// "<path>\t<recognised text>" (empty text = clean).
//
//   swift tools/photo/textcheck.swift a.jpg b.jpg ...
import Foundation
import Vision

for path in CommandLine.arguments.dropFirst() {
    guard let url = Optional(URL(fileURLWithPath: path)),
          let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
        print("\(path)\tERROR unreadable")
        continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    req.minimumTextHeight = 0.012
    try? VNImageRequestHandler(cgImage: img, options: [:]).perform([req])
    let words = (req.results ?? [])
        .compactMap { $0.topCandidates(1).first }
        .filter { $0.confidence >= 0.3 && $0.string.filter(\.isLetter).count >= 2 }
        .map(\.string)
    print("\(path)\t\(words.joined(separator: " | "))")
}
