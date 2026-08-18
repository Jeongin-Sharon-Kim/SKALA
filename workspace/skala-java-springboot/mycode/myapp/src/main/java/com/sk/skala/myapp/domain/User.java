
package com.sk.skala.myapp.domain;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Email;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    
    // private String name;
    // private String email;

    @Positive(message = "ID는 양수입니다")
    private Long id;

    @NotBlank(message = "이름은 필수입니다")
    private String name;

    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;
}











    //public User(){}

    // //생성자, getter 및 setter
    // public User(Long id, String name, String email){
    //     this.id = id;
    //     this.name = name;
    //     this.email = email;
    // }
    // public Long getId(){
    //     return id;
    // }
    // public void setId(Long id){
    //     this.id = id;
    // }
    // public String getName(){
    //     return name;
    // }
    // public void setName(String name){
    //     this.name = name;
    // }
    // public String getEmail(){
    //     return email;
    // }
    // public void setEmail(String email){
    //     this.email = email;
    // }
    
