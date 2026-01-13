import Foundation
import PencilKit

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

struct EditorView: View {
    @State private var text = ""
    @State private var canvas = PKCanvasView()
    @State private var fileURL: URL?

    var body: some View {
        VStack {
            TextEditor(text: $text)
                .frame(height: 150)
                .border(.gray)

            CanvasView(canvas: $canvas)
                .border(.blue)
        }
        .onChange(of: text) { _ in autoSave() }
        .onChange(of: canvas.drawing) { _ in autoSave() }
        .toolbar {
            Button("保存先を選ぶ") {
                pickFile()
            }
        }
    }
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
