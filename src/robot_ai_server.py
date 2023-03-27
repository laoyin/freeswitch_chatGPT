from open_ai.chat_ai import ws_app


if __name__ == "__main__":
    ws_app.run(host="0.0.0.0", port=10889, debug=True)