/* Random number server - lightly modified from the uWebSockets Broadcast example. */
#include "App.h"
#include <random>
#include <iostream>

uWS::App *globalApp;
int port = 9001;
std::random_device rd;
std::uniform_int_distribution<uint32_t> dist;
uint32_t randomNumber = dist(rd);

int main() {
    struct PerSocketData {}; // we don't store any data per socket

    uWS::App app = uWS::App().ws<PerSocketData>("/*", {
        /* Settings */
        .compression = uWS::DISABLED,
        .idleTimeout = 16,
        /* Handlers */
        .upgrade = nullptr,
        .open = [](auto *ws) {
            std::cout << "Client connected\n";
            ws->subscribe("broadcast");
        },
        .close = [](auto */*ws*/, int code, std::string_view message) {
            std::cout << "Client disconnected - code " << code << ", message: '" << message << "'" << std::endl;
        }
    }).listen(port, [](auto *listen_socket) {
        if (listen_socket) {
            std::cout << "Listening on port " << port << std::endl;
        }
    });

    struct us_loop_t *loop = (struct us_loop_t *) uWS::Loop::get();
    struct us_timer_t *delayTimer = us_create_timer(loop, 0, 0);

    std::cout << "Broadcasting random numbers each second..." << std::endl;

    us_timer_set(delayTimer, [](struct us_timer_t */*t*/) {
        std::cout << randomNumber << std::endl;
        globalApp->publish("broadcast", std::string_view((char *) &randomNumber, sizeof(randomNumber)), uWS::OpCode::BINARY, false);
        randomNumber = dist(rd);
    }, 1000, 1000);

    globalApp = &app;

    app.run();
}
