@main
struct MemoApp: App {
    var body: some Scene {
        WindowGroup {
            EditorView()
        }
    }
}

import SwiftUI
import PencilKit

struct EditorView: View {
    @State private var text = ""
    @State private var canvas = PKCanvasView()
    @State private var fileURL: URL?
    @State private var showPicker = false

    var body: some View {
        VStack {
            TextEditor(text: $text)
                .frame(height: 150)
                .border(.gray)

            CanvasView(canvas: $canvas)
                .border(.blue)

            Button("保存先を選ぶ") {
                showPicker = true
            }
        }
        .sheet(isPresented: $showPicker) {
            DocumentPicker { url in
                fileURL = url
                loadFile(url: url)
            }
        }
        .onChange(of: text) { _ in autoSave() }
        .onChange(of: canvas.drawing) { _ in autoSave() }
        .padding()
    }

    func autoSave() {
        guard let url = fileURL else { return }
        let memo = MemoFile(
            text: text,
            drawingData: canvas.drawing.dataRepresentation()
        )
        if let data = try? JSONEncoder().encode(memo) {
            try? data.write(to: url)
        }
    }

    func loadFile(url: URL) {
        if let data = try? Data(contentsOf: url),
           let memo = try? JSONDecoder().decode(MemoFile.self, from: data) {
            text = memo.text
            canvas.drawing = try! PKDrawing(data: memo.drawingData)
        }
    }
}

import SwiftUI
import UniformTypeIdentifiers

struct DocumentPicker: UIViewControllerRepresentable {
    var onPick: (URL) -> Void

    func makeCoordinator() -> Coordinator {
        Coordinator(onPick: onPick)
    }

    func makeUIViewController(context: Context)
        -> UIDocumentPickerViewController {

        let picker = UIDocumentPickerViewController(
            forOpeningContentTypes: [UTType.json]
        )
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(
        _ uiViewController: UIDocumentPickerViewController,
        context: Context
    ) {}

    class Coordinator: NSObject, UIDocumentPickerDelegate {
        var onPick: (URL) -> Void

        init(onPick: @escaping (URL) -> Void) {
            self.onPick = onPick
        }

        func documentPicker(
            _ controller: UIDocumentPickerViewController,
            didPickDocumentsAt urls: [URL]
        ) {
            if let url = urls.first {
                onPick(url)
            }
        }
    }
}
import Foundation

struct MemoFile: Codable {
    var text: String
    var drawingData: Data
}
import SwiftUI
import PencilKit

struct CanvasView: UIViewRepresentable {
    @Binding var canvas: PKCanvasView

    func makeUIView(context: Context) -> PKCanvasView {
        canvas.drawingPolicy = .anyInput
        return canvas
    }

    func updateUIView(_ uiView: PKCanvasView, context: Context) {}
}
