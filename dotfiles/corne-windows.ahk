#Requires AutoHotkey v2.0
#SingleInstance Force

; =============================================================================
; Corne Keyboard Semantic Editing Bridge for Windows (AutoHotkey v2)
;
; Translates semantic F21-F24 signals from Corne NAV/MOUSE layers into standard
; Windows clipboard and undo/redo keyboard shortcuts.
;
; Keyboard emits:      Windows receives:
;   F21            ->    Ctrl+C         (Copy)
;   F22            ->    Ctrl+V         (Paste)
;   F23            ->    Ctrl+X         (Cut)
;   F24            ->    Ctrl+Z         (Undo)
;   Shift+F24      ->    Ctrl+Y         (Redo)
; =============================================================================

; Redo (Shift+F24) must precede bare F24
+F24::Send("^y")

; Undo (F24)
F24::Send("^z")

; Copy (F21)
F21::Send("^c")

; Paste (F22)
F22::Send("^v")

; Cut (F23)
F23::Send("^x")
