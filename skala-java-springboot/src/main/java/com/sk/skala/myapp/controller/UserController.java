package com.sk.skala.myapp.controller;

import org.springframework.web.bind.annotation.*;

import com.sk.skala.myapp.aspect.Metircs.Metrics;
import com.sk.skala.myapp.domain.User;
import com.sk.skala.myapp.service.UserService;

import lombok.extern.slf4j.Slf4j;

import java.util.List;
import java.util.Optional;

@Slf4j
@RestController
@RequestMapping("/api")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService){
        this.userService = userService;
    }

    @Metrics
    // 1. 모든 사용자 조회
    @GetMapping("/users")
    public List<User> getAllUsers(@RequestParam Optional<String> name) {
        log.info("getAllUsers called");
        log.debug("getAllUsers called with name filter: {}", name.orElse("none"));
        return userService.findAll(name);
    }


    // 2. ID로 특정 사용자 조회
    @GetMapping("/users/{id}")
    public User getUserById(@PathVariable long id) {
        return userService.getUserById(id).orElse(null);
    }


    // // 3. name으로 특정 사용자 조회
    // @GetMapping(value = "/users", params = "name")
    // public User getUserByName(@RequestParam("name") String name) {
    //     return userService.getAllUsers().stream()
    //             .filter(user -> user.getName().equals(name))
    //             .findFirst()
    //             .orElse(null);
    // }


    // 4. 사용자 추가
    @PostMapping("/users")
    public User createUser(@RequestBody User user){
        return userService.createUser(user);
    }


    // 5. 사용자 삭제
    @DeleteMapping("/users/{id}")
    public void deleteUser(@PathVariable("id") long id) {
        userService.deleteUser(id);
    }


    // 6. 사용자 정보 수정
    @PutMapping("/users/{id}")
    public User updateUser(
            @PathVariable("id") long id,
            @RequestBody User updatedUser){
            
                return userService.updateUser(id, updatedUser).orElse(null);
    }
}