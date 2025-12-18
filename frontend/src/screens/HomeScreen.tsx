import React from "react";
import { Text, View } from "react-native";

export default function HomeScreen() {
  return (
    <View
      style={{
        flex: 1,
        backgroundColor: "#FFFFFF",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Text style={{ fontSize: 28 }}>HOME SCREEN WORKS</Text>
    </View>
  );
}